from setuptools import setup

setup( 
    name="github-analyzer", 
    version="0.1.0", 
    py_modules=[
        'main',
        'auto_builder',
        'config',
        'constants',
        'decorators',
        'dspy_analyzer',
        'exceptions',
        'github_service',
        'logger'
    ],
    install_requires=[
        "PyGithub>=2.1.1",
        "openai>=1.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "dspy-ai>=2.0.0",
        "pyyaml>=6.0.1",
        "aiohttp>=3.8.0",
    ],
    python_requires=">=3.8",
) 
