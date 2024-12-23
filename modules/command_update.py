from modules.commander import Command, DetectOSCommand
from dotenv import load_dotenv
import os
import logging

load_dotenv()
sudo_password = os.getenv("AV_AGENT_SUDO_PASSWORD")
logger = logging.getLogger("CommandUpdate")


class CommandUpdate(Command):
    def __init__(self):
        logger.debug("CommandUpdate initialized")

    def execute(self, client):
        logger.debug("Executing command update")

        # Detect the OS
        os_command = DetectOSCommand()
        os_id = os_command.execute(client).strip().strip('"')
        logger.info("OS detected: %s", os_id)

        # Determine OS and which update command to use
        if os_id in ["ubuntu", "debian"]:
            logger.debug("OS found: Ubuntu/Debian - using apt")
            update_command = (
                f"echo {sudo_password} | sudo -S apt update && "
                f"echo {sudo_password} | sudo -S apt upgrade -y"
            )
        elif os_id in ["centos", "rhel", "rocky", "fedora"]:
            logger.debug("OS found: CentOS/RHEL/Rocky/Fedora - using yum")
            update_command = f"echo {sudo_password} | sudo -S yum update -y"
        else:
            logger.error("Unsupported OS ID: %s", os_id)
            raise ValueError(f"Unsupported OS ID: {os_id}")

        # Execute command with timeout
        try:
            stdin, stdout, stderr = client.exec_command(
                update_command, timeout=120
            )
            logger.debug("Command executed, waiting for exit status")

            exit_status = stdout.channel.recv_exit_status()
            logger.debug("Exit status: %d", exit_status)

            output = stdout.read().decode()
            error_output = stderr.read().decode()

            if exit_status == 0:
                logger.info("Command executed successfully")
                print(f"Output: {output}")
            else:
                logger.error(
                    "Command execution failed with error: %s", error_output
                )
                print(f"Error: {error_output}")

            return output if exit_status == 0 else None
        except Exception as e:
            logger.exception("Command execution failed")
            print(f"Command execution failed: {e}")
            return None
