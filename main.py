from modules.agent import Agent
from modules.commander import EchoCommand
from modules.command_update import CommandUpdate

if __name__ == "__main__":
    agent = Agent()

    agent.run_ssh_command(EchoCommand("Hello, world!"))
    agent.run_ssh_command(CommandUpdate())
