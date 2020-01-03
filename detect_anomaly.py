import sys
from kapacitor.udf.agent import Agent
from anomaly_detectors import anomaly_detector_hub


if __name__ == '__main__':
    # Create an agent
    agent = Agent()

    # Create a handler and pass it an agent so it can write points
    h = anomaly_detector_hub[sys.argv[1]](agent)

    # Set the handler on the agent
    agent.handler = h

    # Anything printed to STDERR from a UDF process gets captured into the Kapacitor logs.
    print(f"Starting agent for {sys.argv[1]}", file=sys.stderr)
    agent.start()
    agent.wait()
    print("Agent finished", file=sys.stderr)
