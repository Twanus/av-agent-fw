from modules.agent import Agent
from modules.commander import EchoCommand
from modules.command_update import CommandUpdate

# from modules.command_get_logs import CommandGetLogs

if __name__ == "__main__":
    agent = Agent()

    agent.run_ssh_command(EchoCommand("Hello, world!"))
    agent.run_ssh_command(CommandUpdate())
    # agent.run_ssh_command(CommandGetLogs("/var/log/nginx/access.log"))
