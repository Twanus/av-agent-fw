from modules.agent import Agent
from modules.commander import EchoCommand, ListFilesCommand

if __name__ == "__main__":
    agent = Agent()

    text = "Hello, World!"
    agent.run_ssh_command(EchoCommand(text))

    agent.run_ssh_command(ListFilesCommand("/"))
