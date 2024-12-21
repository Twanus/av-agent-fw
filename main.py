import logging
from pathlib import Path
import yaml
from modules import SSHConnector


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

        self.logger.info("Agent initialized successfully")

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
                "repository": "",
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

    def connect_and_run(self, command):
        """Connect to hosts and run a command using SSHConnector."""
        hosts_file = self.config.get("hosts_file")
        private_key_path = self.config.get("private_key_path")

        self.logger.info(
            f"Connecting to hosts from {hosts_file} with private key {private_key_path}"
        )

        try:
            ssh_connector = SSHConnector(hosts_file, private_key_path)
            ssh_connector.run(command)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    agent = Agent()
    agent.connect_and_run("ls -la")
