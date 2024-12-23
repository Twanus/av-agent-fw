import logging
from pathlib import Path
import yaml
from github.GithubException import GithubException
import os
from dotenv import load_dotenv
from modules.ssh_connector import SSHConnector
from modules.commander import Command
from modules.github_client import GitHubClient
import threading

load_dotenv()


class Agent:
    def __init__(self, skip_logging=False):
        # Initialize logging only if not skipped
        if not skip_logging:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(Path("data/agent.log")),
                    logging.StreamHandler(),
                ],
            )
        self.logger = logging.getLogger("AVAgent")

        # Initialize directories (or create when not exists)
        self.config_dir = Path("config")
        self.data_dir = Path("data")
        self.modules_dir = Path("modules")
        self._create_directories()

        # Load config
        self.config = self._load_config()

        # Initialize GitHubClient
        self.github_client = GitHubClient(
            token=os.getenv("AV_AGENT_GITHUB_TOKEN"),
            repository=self.config["repository"],
        )
        self.logger.info("Agent initialized successfully with GitHubClient")

        # Initialize SSHConnector
        self.ssh_connector = SSHConnector(
            self.config["hosts_file"], self.config["private_key_path"]
        )
        self.logger.info("Agent initialized successfully with SSHConnector")

    def _load_config(self):
        """Load config & hosts from GitHub if not found locally."""
        config_file = self.config_dir / "config.yaml"
        hosts_file = self.config_dir / "hosts.txt"

        if not config_file.exists() or not hosts_file.exists():
            missing_files = []
            if not config_file.exists():
                missing_files.append("config.yaml")
            if not hosts_file.exists():
                missing_files.append("hosts.txt")

            self.logger.info(
                f"No local file(s) found: {', '.join(missing_files)}"
            )
            self.logger.info(
                "Attempting to fetch configuration from GitHub repository..."
            )

            try:
                # Initialize GitHub client with minimal config
                self.github_client = GitHubClient(
                    token=os.getenv("AV_AGENT_GITHUB_TOKEN"),
                    repository="Twanus/av-agent-fw",  # Default repository
                )

                config_data = None
                if not config_file.exists():
                    # Fetch config from GitHub
                    config_content = self.github_client.get_file_content(
                        "config/config.yaml"
                    )
                    self.logger.info(
                        "Successfully fetched config.yaml from GitHub"
                    )
                    config_data = yaml.safe_load(config_content)

                if not hosts_file.exists():
                    # Fetch hosts from GitHub
                    hosts_content = self.github_client.get_file_content(
                        "config/hosts.txt"
                    )
                    self.logger.info(
                        "Successfully fetched hosts.txt from GitHub"
                    )
                    self.hosts = hosts_content.splitlines()

                if config_data:
                    return config_data

            except Exception as e:
                self.logger.error(f"Failed to fetch from GitHub: {str(e)}")
                self.logger.info("Using default configuration")
                return {
                    "github_token": "",
                    "repository": "Twanus/av-agent-fw",
                    "check_interval": 300,
                    "enabled_modules": [],
                    "hosts_file": "config/hosts.txt",
                    "private_key_path": "C:/Users/veree/.ssh/id_jacko",
                }

        with open(config_file) as f:
            return yaml.safe_load(f)

    def sync_modules(self):
        """Synchronize modules from GitHub repository."""
        try:
            contents = self.github_client.get_module_contents()
            for content in contents:
                if content.type == "file" and content.name.endswith(".py"):
                    module_path = self.modules_dir / content.name
                    with open(module_path, "wb") as f:
                        f.write(content.decoded_content)
                    self.logger.info(
                        f"Successfully synchronized module: {content.name}"
                    )
        except GithubException as e:
            self.logger.error(f"Failed to sync modules: {str(e)}")
            raise

    def run_ssh_command(self, command: Command):
        """Run a command on this agent's hosts using SSHConnector."""
        hosts = self.ssh_connector.read_hosts()
        for host in hosts:
            client = self.ssh_connector.connect_to_host(host)
            if client:
                output = self.ssh_connector.execute_command(client, command)
                self.ssh_connector.close_connection(client)
                self.logger.info(f"Output from {host}: {output}")
            else:
                self.logger.error(f"Could not connect to {host}")

    def run_ssh_command_async(self, command):
        """Run SSH command asynchronously using SSHConnector."""
        try:
            # Initialize SSHConnector with either hosts list or file path
            if hasattr(self, "hosts"):  # If we loaded hosts from GitHub
                ssh_connector = SSHConnector(
                    private_key_path=self.config.get("private_key_path"),
                    hosts_list=self.hosts,
                )
            else:  # Fall back to hosts file
                ssh_connector = SSHConnector(
                    hosts_file=self.config.get("hosts_file"),
                    private_key_path=self.config.get("private_key_path"),
                )

            # Create and start the thread
            thread = threading.Thread(
                target=self._run_ssh_command_thread,
                args=(ssh_connector, command),
            )
            thread.start()
            return thread

        except Exception as e:
            self.logger.error(f"Failed to run SSH command: {e}")
            return None

    def _execute_on_host(self, host, command: Command):
        """Helper method to execute a command on a single host."""
        client = self.ssh_connector.connect_to_host(host)
        if client:
            output = self.ssh_connector.execute_command(client, command)
            self.ssh_connector.close_connection(client)
            return output
        else:
            raise ConnectionError(f"Could not connect to {host}")

    def _create_directories(self):
        """Ensure all required directories exist."""
        for directory in [self.config_dir, self.data_dir, self.modules_dir]:
            directory.mkdir(exist_ok=True)

    def _run_ssh_command_thread(self, ssh_connector, command):
        """Helper method to run SSH command in a thread."""
        try:
            hosts = ssh_connector.read_hosts()
            self.logger.debug(
                f"Running command '{command}' on {len(hosts)} hosts"
            )

            for host in hosts:
                client, session_id = ssh_connector.connect_to_host(host)
                if client:
                    output = ssh_connector.execute_command(
                        client, command, session_id, host
                    )
                    ssh_connector.close_connection(client, session_id, host)
                    if output:
                        self.logger.info(
                            f"[{session_id}][{host}] Command output: {output}"
                        )
                else:
                    self.logger.error(
                        f"[{session_id}][{host}] Connection failed"
                    )

        except Exception as e:
            self.logger.error(f"Error in SSH command thread: {str(e)}")
