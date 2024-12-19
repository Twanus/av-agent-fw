import logging
from pathlib import Path
import yaml


API_KEY = "trufflehog_please_detect_this_key"

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
                "check_interval": 300,  # 5min
                "enabled_modules": [],
            }
            with open(config_file, "w") as f:
                yaml.dump(default_config, f)
            return default_config

        with open(config_file) as f:
            return yaml.safe_load(f)


if __name__ == "__main__":
    agent = Agent()
