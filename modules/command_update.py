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
            update_command = (
                f"echo {sudo_password} | sudo -S apt update && "
                f"echo {sudo_password} | sudo -S apt upgrade -y"
            )
        elif os_id in ["centos", "rhel", "rocky", "fedora"]:
            update_command = f"echo {sudo_password} | sudo -S yum update -y"
        else:
            raise ValueError(f"Unsupported OS ID: {os_id}")

        try:
            stdin, stdout, stderr = client.exec_command(
                update_command, timeout=120
            )
            exit_status = stdout.channel.recv_exit_status()

            output = stdout.read().decode()
            error_output = stderr.read().decode()

            if exit_status == 0:
                print(f"Output: {output}")
            else:
                print(f"Error: {error_output}")

            return output if exit_status == 0 else None
        except Exception as e:
            print(f"Command execution failed: {e}")
            return None
