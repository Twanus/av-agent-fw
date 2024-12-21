import logging
from pathlib import Path
import yaml
from github import Github
from github.GithubException import GithubException
import os
from dotenv import load_dotenv
from modules.ssh_connector import SSHConnector

load_dotenv()


class Agent:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(Path("data/agent.log")),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("SystemAgent")

        self.config_dir = Path("config")
        self.data_dir = Path("data")
        self.modules_dir = Path("modules")
        self._create_directories()

        self.config = self._load_config()
        self._setup_github_client()

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

    def _setup_github_client(self):
        """Initialize GitHub client with token from environment."""
        token = os.getenv("AV_AGENT_GITHUB_TOKEN")
        if not token:
            self.logger.error("GitHub token is not configured in environment")
            raise ValueError("GitHub token is required but not configured")

        if not self.config["repository"]:
            self.logger.error("GitHub repository is not configured")
            raise ValueError(
                "GitHub repository is required but not configured"
            )

        try:
            self.github = Github(token)
            # Test authentication
            user = self.github.get_user()
            self.logger.info(f"Authenticated as GitHub user: {user.login}")

            self.repo = self.github.get_repo(self.config["repository"])
            self.logger.info(
                f"Successfully connected to repository: {self.config['repository']}"
            )
        except GithubException as e:
            if e.status == 401:
                self.logger.error(
                    "Authentication failed. Please check your GitHub token"
                )
            elif e.status == 404:
                self.logger.error(
                    f"Repository {self.config['repository']} not found"
                )
            else:
                self.logger.error(f"GitHub API error: {str(e)}")
            raise

    def sync_modules(self):
        """Synchronize modules from GitHub repository."""
        try:
            contents = self.repo.get_contents("modules")

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

    def run_ssh_command(self, command):
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
