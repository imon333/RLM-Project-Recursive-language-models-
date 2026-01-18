from src.agent import RLMAgent
from termcolor import colored


def create_test_document():
    """
    Creates a complex document with various challenges:
    - Mixed case keywords
    - Hidden information in different locations
    - Distractors and noise
    """
    doc = ""

    # Part 1: Initial noise (5000 chars)
    doc += ("This is a filler sentence. " * 200)

    # Part 2: First secret (mixed case) around 5000 char mark
    doc += " The secret_project_id is: 'ORION-99' and it's confidential. "

    # Part 3: More noise (10000 chars)
    doc += ("Germany is awesome and very good. " * 300)

    # Part 4: Second secret (different case) around 15000 char mark
    doc += " The SECRET_MOVIE is 'Fury and Peaky Blinders' which are great shows. "

    # Part 5: Even more noise (20000 chars)
    doc += ("This is more noise but not noise. " * 600)

    # Part 6: Third secret (lowercase) deep in document
    doc += " The hidden password is: 'alpha-bravo-charlie-99' for authentication. "

    # Part 7: Final noise (10000 chars)
    doc += ("End of document content here. " * 350)

    return doc


def run_tests():
    """Run multiple test cases to verify the system works"""

    print(colored("=" * 60, "cyan"))
    print(colored("  RECURSIVE LANGUAGE MODEL - ENHANCED VERSION", "cyan", attrs=["bold"]))
    print(colored("=" * 60, "cyan"))

    # Create test document
    massive_context = create_test_document()
    print(f"\n📄 Document created: {len(massive_context)} characters\n")

    # Initialize agent
    agent = RLMAgent(massive_context)

    # Test cases
    test_cases = [
        {
            "name": "Test 1: Case-Insensitive Search",
            "query": "Find the SECRET_PROJECT_ID in the document (search case-insensitive)",
            "expected": "ORION-99"
        },
        {
            "name": "Test 2: Different Case",
            "query": "What is the secret movie mentioned? (it might be in different case)",
            "expected": "Fury and Peaky Blinders"
        },
        {
            "name": "Test 3: Deep Search",
            "query": "Find the hidden password in the document",
            "expected": "alpha-bravo-charlie-99"
        }
    ]

    # Run each test
    for i, test in enumerate(test_cases, 1):
        print("\n" + "=" * 60)
        print(colored(f"\n{test['name']}", "cyan", attrs=["bold"]))
        print(colored(f"Query: {test['query']}", "white"))
        print(colored(f"Expected: {test['expected']}", "yellow"))
        print("=" * 60)

        # Solve
        answer = agent.solve(test['query'])

        # Display result
        print("\n" + "=" * 60)
        print(colored(f"FINAL ANSWER: {answer}", "green" if test['expected'].lower() in answer.lower() else "red",
                      attrs=["bold"]))
        print("=" * 60)

        # Reset agent for next test (new conversation)
        if i < len(test_cases):
            agent = RLMAgent(massive_context)
            print(colored("\n🔄 Resetting agent for next test...\n", "magenta"))


def main():
    """Main entry point"""
    try:
        run_tests()
    except KeyboardInterrupt:
        print(colored("\n\n⚠ Interrupted by user", "red"))
    except Exception as e:
        print(colored(f"\n\n❌ Error: {str(e)}", "red"))
        raise


if __name__ == "__main__":
    main()