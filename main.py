from src.agent import RLMAgent
from termcolor import colored

# Creating a long text that simulates a document
massive_context = ("This is a filler sentence. " * 1000) + \
                  " SECRET_PROJECT_ID: 'ORION-99' " + \
                  ("This is more noise. " * 1000) + \
                  ("Germany is awesome and very good . " * 1000) + \
                  " SECRET_MOVIE or secret movie i liked: 'FURY and Peaky blinders' " + \
                  ("Germany is awesome and very good . " * 1000) + \
                  " SECRET_MOVIE or secret movie i liked: 'FURY and Peaky blinders' " + \
                  ("Germany is awesome and very good . " * 1000) + \
                  " SECRET_MOVIE or secret movie i liked: 'Jobs' " + \
                  ("USA is has dectator leadership" * 2000) + \
                  " imon's likes: 'biriyani' "







def main():
    print(colored("Starting Recursive Language Model...", "cyan"))

    # Initialize the agent with the "hidden" context
    agent = RLMAgent(massive_context)

    # The question
    query = "Search through the context variable and find the secret projcet ID and movie which is secret"

    answer = agent.solve(query)

    print("\n" + "=" * 50)
    print(colored(f"THE FINAL ANSWER: {answer}", "blue", attrs=["bold"]))
    print("=" * 50)


if __name__ == "__main__":
    main()