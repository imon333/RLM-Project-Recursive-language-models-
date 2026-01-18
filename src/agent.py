#agent
# the main brain that orchestrates the loop

import re
from termcolor import colored
from src.llm_client import get_llm_response
from src.repl import RLMREPL
from src.prompts import RLM_SYSTEM_PROMPT


class RLMAgent:
    def __init__(self, context):
        """ Initialize agent with context and REPL environment"""
        self.repl = RLMREPL(context)

        # Format the system prompt with context info
        formatted_prompt = RLM_SYSTEM_PROMPT.format(context_total_length=len(context))

        self.history = [{"role": "system", "content": formatted_prompt}]
        self.max_iterations = 10 #

    def solve(self, user_query):
        self.history.append({"role": "user", "content": f"Task: {user_query}"})

        for i in range(self.max_iterations):
            print(colored(f"\n--- Iteration {i + 1} ---", "magenta", attrs=["bold"]))

            # 1. Root Model decides what to do
            ai_thought = get_llm_response(self.history, role="root")
            print(colored(f"Root LM Thought:\n{ai_thought}", "green"))
            self.history.append({"role": "assistant", "content": ai_thought})

            # 2. Check for final answer
            final_match = re.search(r"FINAL\((.*?)\)", ai_thought, re.DOTALL)
            if final_match:
                answer = final_match.group(1).strip()
                print(colored(f"\n✓ Found final answer in iteration {i + 1}", "cyan"))
                return answer

            # 3. Extract and execute code
            code_match = re.search(r"```python(.*?)```", ai_thought, re.DOTALL)

            if code_match:
                code = code_match.group(1).strip()

                # Show the code being executed
                print(colored("Executing code:", "yellow"))
                print(colored(code[:200] + "..." if len(code) > 200 else code, "white"))

                # Run it
                result = self.repl.run_code(code)

                # Show result (truncated if too long)
                display_result = result[:500] + "..." if len(result) > 500 else result
                print(colored(f"REPL Output: {display_result}", "yellow"))

                # Feed result back to AI
                self.history.append({
                    "role": "user",
                    "content": f"Observation: {result}"
                })
            else:
                # No code provided
                print(colored("⚠ No code block found. AI should write code!", "red"))

                # Prompt the AI to take action
                self.history.append({
                    "role": "user",
                    "content": "You must write Python code in a ```python ``` block to solve this task. Use the search() function to find keywords."
                })

        # If we exit the loop without finding answer
        print(colored(f"\n✗ Reached maximum iterations ({self.max_iterations})", "red"))
        return "Task could not be completed - maximum iterations reached. Consider: 1) Is the information actually in the document? 2) Try different search terms."