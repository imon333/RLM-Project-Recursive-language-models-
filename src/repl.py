#repl
import io
import re
import sys
from termcolor import colored
from src.llm_client import get_llm_response

class RLMREPL:
    def __init__(self, context_text):
        """ Initialize the REPL environment with enhanced search tools"""

        # Store the original context
        self.context_text = context_text

        # Enhanced environment with smart search tools

        self.env_locals = {
            "context": context_text,
            "llm_query": self.sub_lm_worker,
            "print": print,

            # NEW: Smart search functions
            "search": self.smart_search,
            "search_all": self.search_all_occurrences,
            "extract_around": self.extract_around_keyword,

        }

    def smart_search(self, keyword, case_sensitive=False):
        """ Smart search that finds keyword regardless of case (by default)
        Args:
            keyword: The text to search for
            case_sensitive: If true,  match exact case (default: False)

        Returns:
            Index of first occurrence , or -1 if not found
        """

        if case_sensitive:
            return self.context_text.find(keyword)
        else:
            # Case-insensitive search

            lower_context = self.context_text.lower()
            lower_keyword = keyword.lower()
            return lower_keyword.find(lower_context)


    def search_all_occurrences(self, keyword, case_sensitive=False):

        """
        Find ALL occurrences of a keyword
        Returns:
            List of (index, matched_text) tuples

        """
        results = []

        if case_sensitive:
            pattern = re.compile(keyword)
        else:
            pattern = re.compile(keyword)
            flags = re.IGNORECASE

        # Find all matches
        for match in re.finditer(pattern, self.context_text, flags=0 if case_sensitive else re.IGNORECASE):
            results.append({
                "index": match.start(),
                "text": match.group(),
                "context": self.context_text[max(0, match.start()):match.end()+50]
            })
        return results

    def extract_around_keyword(self, keyword, chars_before=100, chars_after=100, case_sensitive=False):
        """
        Extract text around a keyword (context window)

        Args:
            keyword: What to search for
            chars_before: Characters before the keyword
            chars_after: Characters after the keyword
            case_sensitive: Exact case matching

        Returns:
            String with context around the keyword, or None if not found

        """
        index = self.smart_search(keyword, case_sensitive)
        if index == -1:
            return None

        start = max(0, index - chars_before)
        end = min(len(self.context_text), index + len(keyword) + chars_after)

        return self.context_text[start:end]


    def sub_lm_worker(self, task_description):
        """
        Sub-LLM worker that analyzes specific chunks
        Now receives better context from smart search functions
        """
        print(colored(f"  [Sub-LM Worker] Analyzing: {task_description[:80]}...", "blue"))

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