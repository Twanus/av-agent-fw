from modules.agent import Agent
from modules.commander import EchoCommand
import logging
import argparse


def setup_logging(log_level):
    """Configure logging for all modules"""
    # Clear any existing handlers to avoid duplication
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("data/agent.log"),
            logging.StreamHandler(),
        ],
    )

    # Ensure all existing loggers respect the new level
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).setLevel(log_level)


def main():
    logger = logging.getLogger("Main")
    logger.info("Starting main script")
    agent = Agent(skip_logging=True)

    # agent.run_ssh_command(EchoCommand("Hello, world!"))
    # agent.run_ssh_command_async(CommandUpdate())
    # agent.run_ssh_command_async(CommandGetLogs("/var/log/nginx/access.log"))
    agent.run_ssh_command_async(EchoCommand("Hello, world!"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run main.py with a specific logging level."
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Set the logging level (e.g., DEBUG, INFO, WARNING)",
    )
    args = parser.parse_args()

    # Configure logging
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)
    setup_logging(log_level)

    main()
