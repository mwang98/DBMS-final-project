import sys

from kapacitor.udf.agent import Agent
from handler import CustomHandler


if __name__ == '__main__':
    # Create an agent
    agent = Agent()

    # Create a handler and pass it an agent so it can write points
    h = CustomHandler(agent)

    # Set the handler on the agent
    agent.handler = h

    # Anything printed to STDERR from a UDF process gets captured into the Kapacitor logs.
    print(f"Starting agent...", file=sys.stderr)
    agent.start()
    agent.wait()
    print("Agent finished.", file=sys.stderr)
