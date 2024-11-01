from github import Github, GithubException
import requests
from pathlib import Path
from typing import Tuple, Optional, Dict
import shutil
from config import Config
from logger import setup_logger

class GitHubServiceError(Exception):
    """Base exception for GitHub service errors"""
    pass

class GitHubService:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, log_dir=config.LOG_DIRECTORY)
        try:
            self.github = Github(config.GITHUB_TOKEN)
            self.validate_token()
        except Exception as e:
            raise GitHubServiceError(f"Failed to initialize GitHub service: {str(e)}")

    def validate_token(self) -> bool:
        """Validate GitHub token is present and valid"""
        try:
            self.github.get_user().login
            self.logger.info("GitHub token validated successfully")
            return True
        except GithubException as e:
            self.logger.error(f"Invalid GitHub token: {e.data.get('message', str(e))}")
            raise GitHubServiceError(f"Invalid GitHub token: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error validating token: {str(e)}")
            raise GitHubServiceError(f"Token validation failed: {str(e)}")

    def download_repository(self, repo_url: str) -> Tuple[Optional[Path], Optional[object]]:
        """Download repository contents"""
        try:
            # Extract owner and repo name from URL
            url_parts = repo_url.replace("https://github.com/", "").split('/')
            if len(url_parts) != 2:
                raise GitHubServiceError("Invalid GitHub repository URL format")
                
            owner, repo_name = url_parts
            self.logger.info(f"Attempting to download repository: {owner}/{repo_name}")
            
            try:
                repo = self.github.get_repo(f"{owner}/{repo_name}")
            except GithubException as e:
                self.logger.error(f"Failed to access repository: {e.data.get('message', str(e))}")
                raise GitHubServiceError(f"Repository access failed: {str(e)}")

            # Create repository directory
            repo_path = Path(self.config.BASE_DIRECTORY) / repo_name
            
            # Clean existing directory if present
            if repo_path.exists():
                self.logger.info(f"Removing existing repository at {repo_path}")
                shutil.rmtree(repo_path)
            
            repo_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {repo_path}")

            self._download_contents(repo, repo.get_contents(""), repo_path)
            self.logger.info(f"Repository downloaded successfully to {repo_path}")
            
            return repo_path, repo
            
        except GitHubServiceError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error downloading repository: {str(e)}")
            raise GitHubServiceError(f"Repository download failed: {str(e)}")

    def _download_contents(self, repo, contents, current_path: Path):
        """Recursively download repository contents"""
        for content_file in contents:
            try:
                file_path = current_path / content_file.name
                
                if content_file.type == "dir":
                    file_path.mkdir(exist_ok=True)
                    self._download_contents(repo, repo.get_contents(content_file.path), file_path)
                    self.logger.debug(f"Created directory: {file_path}")
                else:
                    response = requests.get(content_file.download_url)
                    response.raise_for_status()
                    
                    file_path.write_bytes(response.content)
                    self.logger.debug(f"Downloaded file: {file_path}")
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to download {content_file.path}: {str(e)}")
                raise GitHubServiceError(f"Failed to download {content_file.path}: {str(e)}")
            except Exception as e:
                self.logger.error(f"Error processing {content_file.path}: {str(e)}")
                raise GitHubServiceError(f"Error processing {content_file.path}: {str(e)}")

    def get_readme_content(self, repo) -> Optional[str]:
        """Get README content from repository"""
        try:
            readme = repo.get_readme()
            self.logger.info("README file found and retrieved")
            return readme.decoded_content.decode('utf-8')
        except GithubException as e:
            self.logger.warning(f"README not found: {e.data.get('message', str(e))}")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving README: {str(e)}")
            return None