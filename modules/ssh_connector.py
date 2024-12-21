import paramiko
import logging
from modules.commander import Command
import os


class SSHConnector:
    def __init__(self, hosts_file, private_key_path):
        self.logger = logging.getLogger(__name__)
        self.hosts_file = hosts_file
        self.private_key_path = private_key_path
        self.known_hosts_file = os.path.expanduser("~/.ssh/known_hosts")

    def read_hosts(self):
        with open(self.hosts_file, "r") as file:
            hosts = file.read().splitlines()
        return hosts

    def connect_to_host(self, host):
        try:
            self.logger.info(f"Connecting to {host}...")
            key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
            client = paramiko.SSHClient()
            # First try to load known hosts
            if os.path.exists(self.known_hosts_file):
                client.load_system_host_keys(self.known_hosts_file)

            # Use WarningPolicy() as a middle ground - warn but no block
            client.set_missing_host_key_policy(paramiko.WarningPolicy())

            client.connect(
                hostname=host,
                username="jacko",
                pkey=key,
                allow_agent=False,
                look_for_keys=False,
            )

            self.logger.info(f"Connected to {host}")
            return client
        except paramiko.SSHException as ssh_err:
            self.logger.error(f"SSH error connecting to {host}: {ssh_err}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to connect to {host}: {e}")
            return None

    def execute_command(self, client, command: Command):
        try:
            output = command.execute(client)
            return output
        except Exception as e:
            self.logger.error(f"Failed to execute command: {e}")
            return None

    def close_connection(self, client: paramiko.SSHClient):
        self.logger.info("Connection closed.")
        client.close()

    def connect_and_run(self, command: Command):
        """Connect to hosts and run a command using SSHConnector."""
        hosts_file = self.config.get("hosts_file")
        private_key_path = self.config.get("private_key_path")
        try:
            ssh_connector = SSHConnector(hosts_file, private_key_path)
            ssh_connector.run(command)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
