# Standard library imports
import os
import sys
import json
from typing import Dict, List, Optional, Union
import asyncio
import openai
from pathlib import Path
import subprocess

# Third-party imports
from decorators import cache_result, retry_on_failure
from logger import setup_logger
from dspy_analyzer import DSPyAnalyzer
from constants import BuildStepType
from exceptions import BuildError

class AutoBuilder:
    """Handles the automated building of repositories based on analysis."""
    
    def __init__(self, config):
        self.config = config
        openai.api_key = config.OPENAI_API_KEY
        self.logger = setup_logger(__name__, log_dir=config.LOG_DIRECTORY)
        self.dspy_analyzer = DSPyAnalyzer(config)

    @cache_result(Path("cache/analysis"))
    @retry_on_failure()
    async def analyze_build_steps(self, readme_content: str) -> Optional[Dict]:
        """
        Analyze README content using DSPy and OpenAI.
        
        Args:
            readme_content: Content of the README file
            
        Returns:
            Optional[Dict]: Analysis results or None if analysis fails
            
        Raises:
            BuildError: If analysis fails critically
        """
        try:
            dspy_analysis = await self.dspy_analyzer.analyze_readme(readme_content)
            
            if not dspy_analysis:
                self.logger.warning("DSPy analysis failed, falling back to OpenAI")
                return await self._get_openai_analysis(readme_content)
                
            return dspy_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing build steps: {e}")
            raise BuildError(f"Build analysis failed: {str(e)}")

    async def execute_build_steps(self, repo_path: Path, build_instructions: Dict) -> bool:
        """
        Execute build steps asynchronously.
        
        Args:
            repo_path: Path to repository
            build_instructions: Dictionary containing build instructions
            
        Returns:
            bool: True if build succeeds, False otherwise
            
        Raises:
            BuildError: If build fails critically
        """
        try:
            self.logger.info("Installing dependencies...")
            if not await self._install_dependencies(build_instructions.get('dependencies', [])):
                return False

            steps = [
                (BuildStepType.SETUP, build_instructions.get('setup_steps', [])),
                (BuildStepType.BUILD, build_instructions.get('build_steps', [])),
                (BuildStepType.TEST, build_instructions.get('test_steps', []))
            ]

            for step_type, step_list in steps:
                self.logger.info(f"\nExecuting {step_type.value} steps...")
                if not await self._execute_steps(repo_path, step_list):
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error executing build steps: {e}")
            raise BuildError(f"Build execution failed: {str(e)}")

    async def _install_dependencies(self, dependencies: List[str]) -> bool:
        """Install dependencies asynchronously"""
        try:
            for dep in dependencies:
                cmd = f"pip install {dep}"
                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    self.logger.error(f"Failed to install {dep}: {stderr.decode()}")
                    return False
                    
            return True
        except Exception as e:
            self.logger.error(f"Error installing dependencies: {e}")
            return False

    async def _execute_steps(self, repo_path: Path, steps: List[Dict]) -> bool:
        """Execute a set of build steps"""
        for step in steps:
            self.logger.info(f"\nExecuting: {step['description']}")
            try:
                process = await asyncio.create_subprocess_shell(
                    step['command'],
                    cwd=repo_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    self.logger.error(f"Step failed: {stderr.decode()}")
                    return False
                    
                self.logger.debug(f"Output: {stdout.decode()}")
            except Exception as e:
                self.logger.error(f"Error executing step: {e}")
                return False
                
        return True