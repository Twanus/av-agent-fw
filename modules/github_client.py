from github import Github
from github.GithubException import GithubException
import logging

# Create logger at module level
logger = logging.getLogger("GitHubClient")


class GitHubClient:
    def __init__(self, token, repository):
        self.token = token
        self.repository_name = repository
        self.github = None
        self.repo = None
        logger.debug(
            "Initializing GitHubClient for repository: %s", repository
        )
        self._authenticate()

    def _authenticate(self):
        logger.debug("Attempting to authenticate with GitHub")
        try:
            self.github = Github(self.token)
            user = self.github.get_user()
            logger.info(f"Authenticated as GitHub user: {user.login}")
            logger.debug("Attempting to connect to repository")
            self.repo = self.github.get_repo(self.repository_name)
            logger.info(
                f"Successfully connected to repository: {self.repository_name}"
            )
        except GithubException as e:
            logger.debug(
                "Authentication failed with status code: %d", e.status
            )
            self._handle_github_exception(e)
            raise

    def _handle_github_exception(self, e):
        if e.status == 401:
            logger.error(
                "Authentication failed. Please check your GitHub token"
            )
        elif e.status == 404:
            logger.error(f"Repository {self.repository_name} not found")
        else:
            logger.error(f"GitHub API error: {str(e)}")
        logger.debug("Full exception data: %s", e.data)

    def get_module_contents(self, path="modules"):
        logger.debug("Fetching contents from path: %s", path)
        try:
            contents = self.repo.get_contents(path)
            logger.debug(
                "Successfully retrieved %d items from %s", len(contents), path
            )
            return contents
        except GithubException as e:
            logger.error(f"Failed to get contents from GitHub: {str(e)}")
            logger.debug(
                "Error details - Status: %d, Data: %s", e.status, e.data
            )
            raise

    def get_file_content(self, path):
        """Fetch raw content of a file from GitHub."""
        logger.info(f"Fetching file content from path: {path}")
        try:
            content = self.repo.get_contents(path)
            if isinstance(content, list):
                raise ValueError(f"Path {path} is a directory, not a file")

            logger.debug(f"Successfully retrieved file: {path}")
            return content.decoded_content.decode("utf-8")
        except GithubException as e:
            logger.error(f"Failed to get file content from GitHub: {str(e)}")
            logger.debug(f"Error details - Status: {e.status}, Data: {e.data}")
            raise
