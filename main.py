import asyncio
from pathlib import Path
import json
import sys
from github_service import GitHubService, GitHubServiceError
from auto_builder import AutoBuilder
from config import Config
from logger import setup_logger
from exceptions import BuildError

logger = setup_logger(__name__)

async def compare_repositories(repo1_path: Path, repo2_path: Path) -> list:
    """Find missing files between 2 repos"""
    try:
        repo1_files = set(f.relative_to(repo1_path) for f in repo1_path.rglob('*') if f.is_file())
        repo2_files = set(f.relative_to(repo2_path) for f in repo2_path.rglob('*') if f.is_file())
        return list(repo1_files - repo2_files)
    except Exception as e:
        logger.error(f"Error comparing repositories: {str(e)}")
        return []

async def run_project(repo_url1: str, repo_url2: str = None):
    """Run the full project"""
    try:
        config = Config.from_yaml()
        config.validate()
        
        github_service = GitHubService(config)
        auto_builder = AutoBuilder(config)

        logger.info(f"Processing repository 1: {repo_url1}")
        try:
            repo1_path, repo1 = await github_service.download_repository(repo_url1)
            if not repo1_path or not repo1:
                logger.error("Failed to download repository 1")
                return
        except GitHubServiceError as e:
            logger.error(f"Failed to process repository 1: {str(e)}")
            return
        
        readme_content = await github_service.get_readme_content(repo1)
        if not readme_content:
            logger.warning("No README found in repository")
            return

        try:
            build_instructions = await auto_builder.analyze_build_steps(readme_content)
            if not build_instructions:
                logger.warning("No build instructions found in README")
                return

            logger.info("\nAnalyzed build instructions:")
            logger.info(json.dumps(build_instructions, indent=2))

            if await auto_builder.execute_build_steps(repo1_path, build_instructions):
                logger.info("\nRepository built successfully!")
            else:
                logger.error("\nRepository build failed!")
        except BuildError as e:
            logger.error(f"Build process failed: {str(e)}")
        
        if repo_url2:
            logger.info(f"\nProcessing repository 2: {repo_url2}")
            try:
                repo2_path, repo2 = await github_service.download_repository(repo_url2)
                if repo2_path:
                    missing_files = await compare_repositories(repo1_path, repo2_path)
                    if missing_files:
                        logger.info("\nMissing files:")
                        for file in missing_files:
                            logger.info(f"  - {file}")
                    else:
                        logger.info("\nNo missing files found")
            except GitHubServiceError as e:
                logger.error(f"Failed to process repository 2: {str(e)}")

    except Exception as e:
        logger.error(f"Critical error running project: {str(e)}")
        sys.exit(1)

def main():
    try:
        repo_url = input("Enter the GitHub repository URL to analyze and build: ").strip()
        if not repo_url:
            logger.error("Repository URL is required")
            return
            
        repo_url2 = input("Enter second repository URL for comparison (optional, press Enter to skip): ").strip()
        asyncio.run(run_project(repo_url, repo_url2 if repo_url2 else None))
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

