from github import Github
from github.GithubException import GithubException
import logging


class GitHubClient:
    def __init__(self, token, repository):
        self.logger = logging.getLogger(__name__)
        self.token = token
        self.repository_name = repository
        self.github = None
        self.repo = None
        self._authenticate()

    def _authenticate(self):
        try:
            self.github = Github(self.token)
            user = self.github.get_user()
            self.logger.info(f"Authenticated as GitHub user: {user.login}")
            self.repo = self.github.get_repo(self.repository_name)
            self.logger.info(
                f"Successfully connected to repository: {self.repository_name}"
            )
        except GithubException as e:
            self._handle_github_exception(e)
            raise

    def _handle_github_exception(self, e):
        if e.status == 401:
            self.logger.error(
                "Authentication failed. Please check your GitHub token"
            )
        elif e.status == 404:
            self.logger.error(f"Repository {self.repository_name} not found")
        else:
            self.logger.error(f"GitHub API error: {str(e)}")

    def get_module_contents(self, path="modules"):
        try:
            return self.repo.get_contents(path)
        except GithubException as e:
            self.logger.error(f"Failed to get contents from GitHub: {str(e)}")
            raise
