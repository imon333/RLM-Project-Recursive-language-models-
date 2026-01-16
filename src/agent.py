# the main brain that orchestrates the loop

import re
from termcolor import colored
from src.llm_client import get_llm_response
from src.repl import RLMREPL
from src.prompts import RLM_SYSTEM_PROMPT


class RLMAgent:
    def __init__(self, context):
        self.repl = RLMREPL(context)
        self.history = [{"role": "system", "content": RLM_SYSTEM_PROMPT}]

    def solve(self, user_query):
        self.history.append({"role": "user", "content": f"Task: {user_query}"})

        for i in range(5):  # Limit to 5 steps to save tokens/money
            print(colored(f"\n--- Iteration {i + 1} ---", "magenta", attrs=["bold"]))

            # 1. Root Model decides what to do
            ai_thought = get_llm_response(self.history, role="root")
            print(colored(f"Root LM Thought:\n{ai_thought}", "green"))
            self.history.append({"role": "assistant", "content": ai_thought})

            # 2. Check for final answer
            if "FINAL(" in ai_thought:
                return re.search(r"FINAL\((.*?)\)", ai_thought).group(1)

            # 3. Extract and execute code
            code_match = re.search(r"```python(.*?)```", ai_thought, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
                result = self.repl.run_code(code)
                print(colored(f"REPL Output: {result}", "yellow"))
                self.history.append({"role": "user", "content": f"Observation: {result}"})
            else:
                print(colored("No code provided by AI. Stopping.", "red"))
                break
        return "Task could not be completed in time."
