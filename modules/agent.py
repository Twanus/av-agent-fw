import logging
from pathlib import Path
import yaml
from github.GithubException import GithubException
import os
from dotenv import load_dotenv
from modules.ssh_connector import SSHConnector
from modules.commander import Command
from modules.github_client import GitHubClient

load_dotenv()


class Agent:
    def __init__(self):
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(Path("data/agent.log")),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("SystemAgent")

        # Initialize directories
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

    def _create_directories(self):
        """Ensure all required directories exist."""
        for directory in [self.config_dir, self.data_dir, self.modules_dir]:
            directory.mkdir(exist_ok=True)

    def _load_config(self):
        """Load the main configuration file."""
        config_file = self.config_dir / "config.yaml"
        if not config_file.exists():
            self.logger.warning(
                "No configuration file found. Creating default config."
            )
            default_config = {
                "github_token": "",
                "repository": "Twanus/av-agent-fw",
                "check_interval": 300,
                "enabled_modules": [],
                "hosts_file": "config/hosts.txt",
                "private_key_path": "C:/Users/veree/.ssh/id_jacko",
            }
            with open(config_file, "w") as f:
                yaml.dump(default_config, f)
            return default_config

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