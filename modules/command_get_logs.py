from modules.commander import Command
from dotenv import load_dotenv
import os

load_dotenv()

sudo_password = os.getenv("AV_AGENT_SUDO_PASSWORD")


class CommandGetLogs(Command):
    def __init__(self, log_path):
        self.log_path = log_path

    def execute(self, client):
        command = f"echo {sudo_password} | sudo -S cat {self.log_path}"
        try:
            stdin, stdout, stderr = client.exec_command(command)
            stdin.write(sudo_password + "\n")
            stdin.flush()
            output = stdout.read().decode()
            error_output = stderr.read().decode()

            if stdout.channel.recv_exit_status() == 0:
                return output
            else:
                print(f"Error retrieving logs: {error_output}")
                return None

        except Exception as e:
            print(f"Command execution failed: {e}")
            return None
