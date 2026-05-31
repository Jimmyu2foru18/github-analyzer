import asyncio
from github_service import GitHubService
from auto_builder import AutoBuilder
from config import Config
from logger import setup_logger

class ScannerService:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, log_dir=config.LOG_DIRECTORY)
        self.github_service = GitHubService(config)
        self.auto_builder = AutoBuilder(config)

    async def scan_and_audit(self, keyword: str):
        self.logger.info(f"Starting scan for: {keyword}")
        repos = self.github_service.search_repositories(keyword)
        
        for repo_full_name in repos:
            self.logger.info(f"Processing: {repo_full_name}")
            try:
                repo_url = f"https://github.com/{repo_full_name}"
                repo_path, repo = await self.github_service.download_repository(repo_url)
                if not repo:
                    continue
                
                readme_content = await self.github_service.get_readme_content(repo)
                if not readme_content:
                    continue
                    
                build_instructions = await self.auto_builder.analyze_build_steps(readme_content)
                if build_instructions:
                    self.logger.info(f"Successfully audited {repo_full_name}")
                    # In future, automatically fix or suggest fixes
                
            except Exception as e:
                self.logger.error(f"Error processing {repo_full_name}: {e}")
