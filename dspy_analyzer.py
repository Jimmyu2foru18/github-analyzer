import dspy
from typing import Dict, Optional, List
from pathlib import Path
from decorators import cache_result, retry_on_failure
from logger import setup_logger
from config import Config

class DSPyAnalyzer:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, log_dir=config.LOG_DIRECTORY)
        # Initialize DSPy with preferred model
        dspy.settings.configure(model=config.MODEL_NAME)
        
    class ReadmeAnalyzer(dspy.Signature):
        """Analyze README content for build instructions"""
        input_readme = dspy.InputField(desc="README content to analyze")
        dependencies = dspy.OutputField(desc="List of required dependencies")
        setup_steps = dspy.OutputField(desc="List of setup commands and descriptions")
        build_steps = dspy.OutputField(desc="List of build commands and descriptions")
        test_steps = dspy.OutputField(desc="List of test commands and descriptions")

    async def analyze_readme(self, readme_content: str) -> Optional[Dict]:
        """Analyze README using DSPy"""
        try:
            analyzer = dspy.Predict(self.ReadmeAnalyzer)
            result = analyzer(input_readme=readme_content)
            
            return {
                "dependencies": result.dependencies,
                "setup_steps": self._parse_steps(result.setup_steps),
                "build_steps": self._parse_steps(result.build_steps),
                "test_steps": self._parse_steps(result.test_steps)
            }
        except Exception as e:
            self.logger.error(f"Error in DSPy analysis: {e}")
            return None
            
    def _parse_steps(self, steps_str: str) -> List[Dict]:
        """Parse steps string into structured format"""
        steps = []
        for step in steps_str.split('\n'):
            if ':' in step:
                command, description = step.split(':', 1)
                steps.append({
                    "command": command.strip(),
                    "description": description.strip()
                })
        return steps