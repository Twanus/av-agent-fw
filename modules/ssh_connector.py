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
        """Reads the hosts from the specified hosts file."""
        try:
            with open(self.hosts_file, "r") as file:
                hosts = file.read().splitlines()
            self.logger.info(f"Loaded hosts from {self.hosts_file}")
            return hosts
        except FileNotFoundError:
            self.logger.error(f"Hosts file {self.hosts_file} not found.")
            return []
        except Exception as e:
            self.logger.error(
                f"Error reading hosts file {self.hosts_file}: {e}"
            )
            return []

    def add_host_key(self, client, hostname):
        host_key = client.get_transport().get_remote_server_key()
        host_keys = paramiko.HostKeys()
        if os.path.exists(self.known_hosts_file):
            host_keys.load(self.known_hosts_file)
        host_keys.add(hostname, host_key.get_name(), host_key)
        host_keys.save(self.known_hosts_file)
        self.logger.info(f"Host key for {hostname} added to known_hosts.")

    def connect_to_host(self, host):
        client = paramiko.SSHClient()
        try:
            key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
            if os.path.exists(self.known_hosts_file):
                client.load_system_host_keys(self.known_hosts_file)

            client.set_missing_host_key_policy(paramiko.RejectPolicy())

            client.connect(
                hostname=host,
                username="jacko",
                pkey=key,
                allow_agent=False,
                look_for_keys=False,
            )
            self.add_host_key(client, host)
            self.logger.info(f"Connected to {host}.")
            return client
        except paramiko.SSHException as ssh_err:
            self.logger.error(f"SSH error connecting to {host}: {ssh_err}")
        except Exception as e:
            self.logger.error(f"Failed to connect to {host}: {e}")
        return None

    def execute_command(self, client, command: Command):
        if client is None:
            self.logger.error("SSH client is None, cannot execute command.")
            return None
        try:
            output = command.execute(client)
            return output
        except Exception as e:
            self.logger.error(f"Failed to execute command: {e}")
            return None

    def close_connection(self, client):
        if client:
            client.close()
            self.logger.info("Connection closed.")

    def connect_and_run(self, command: Command):
        """Connect to hosts and run a command using SSHConnector."""
        hosts_file = self.config.get("hosts_file")
        private_key_path = self.config.get("private_key_path")
        try:
            ssh_connector = SSHConnector(hosts_file, private_key_path)
            ssh_connector.run(command)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
