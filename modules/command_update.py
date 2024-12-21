from modules.commander import Command, DetectOSCommand
from dotenv import load_dotenv
import os

load_dotenv()

sudo_password = os.getenv("AV_AGENT_SUDO_PASSWORD")


class CommandUpdate(Command):
    def execute(self, client):
        # Detect the OS
        os_command = DetectOSCommand()
        os_id = os_command.execute(client).strip().strip('"')
        print("os_id", os_id)

        # Determine the update command based on the OS
        if os_id in ["ubuntu", "debian"]:
            update_command = f"echo {sudo_password} | sudo -S apt update && sudo apt upgrade -y"
        elif os_id in ["centos", "rhel", "rocky", "fedora"]:
            update_command = f"echo {sudo_password} | sudo -S yum update -y"
        else:
            raise ValueError(f"Unsupported OS ID: {os_id}")

        # Execute the update command
        stdin, stdout, stderr = client.exec_command(update_command)

        # Wait for the command to complete
        exit_status = stdout.channel.recv_exit_status()

        # Read the output
        output = stdout.read().decode()
        error_output = stderr.read().decode()

        if exit_status == 0:
            print(f"Output: {output}")
        else:
            print(f"Error: {error_output}")
            # You can add notification logic here if needed

        return output if exit_status == 0 else None
