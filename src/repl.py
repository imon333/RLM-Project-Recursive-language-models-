#repl
import io
import sys
from termcolor import colored
from src.llm_client import get_llm_response

class RLMREPL:
    def __init__(self, context_text):
        # Storing the massive context here in a local dictionary

        self.env_locals = {
            "context": context_text,
            "llm_query": self.sub_lm_worker,
            "print": print
        }

    def sub_lm_worker(self, task_description):
        """ This function is what the 'Root' model calls inside its Python code. """
        print(colored(f" [Sub-LM Worker] Thinking about:{task_description[:60]}", "blue"))
        messages = [{"role": "user", "content": task_description}]
        return get_llm_response(messages, role="sub")

    def run_code(self, code):
        """ Executes code and captures what was printed to the console"""
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            exec(code,{}, self.env_locals)
            output = buffer.getvalue()
        except Exception as e:
            output = f"Python Error:{str(e)}"
        finally:
            sys.stdout = sys.__stdout__ # reset stdout
        return output