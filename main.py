from modules.agent import Agent
from modules.commander import EchoCommand

if __name__ == "__main__":
    agent = Agent()

    agent.run_ssh_command(EchoCommand("Hello, world!"))
