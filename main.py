from modules.agent import Agent
from modules.commander import PlainCommand

if __name__ == "__main__":
    agent = Agent()

    agent.run_ssh_command(PlainCommand("cat /etc/os-release"))
