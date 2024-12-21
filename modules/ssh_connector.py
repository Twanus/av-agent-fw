import paramiko
import logging
from pathlib import Path


class SSHConnector:
    def __init__(self, hosts_file, private_key_path):
        self.logger = logging.getLogger(__name__)
        self.hosts_file = hosts_file
        self.private_key_path = private_key_path

    def read_hosts(self):
        with open(self.hosts_file, "r") as file:
            hosts = file.read().splitlines()
        return hosts

    def connect_to_host(self, host):
        try:
            self.logger.info(f"Connecting to {host}...")
            key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host, username="jacko", pkey=key)
            self.logger.info(f"Connected to {host}")
            return client
        except Exception as e:
            self.logger.error(f"Failed to connect to {host}: {e}")
            return None

    def execute_command(self, client, command):
        try:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            self.logger.info(f"Command output: {output}")
            return output
        except Exception as e:
            self.logger.error(f"Failed to execute command: {e}")
            return None

    def close_connection(self, client):
        client.close()
        self.logger.info("Connection closed.")

    def run(self, command):
        hosts = self.read_hosts()
        for host in hosts:
            client = self.connect_to_host(host)
            if client:
                self.execute_command(client, command)
                self.close_connection(client)
