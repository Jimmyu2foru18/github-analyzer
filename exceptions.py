class GitHubAnalyzerError(Exception):
    """Base exception for GitHub Analyzer errors"""
    pass

class ConfigurationError(GitHubAnalyzerError):
    """Configuration related errors"""
    pass

class GitHubServiceError(GitHubAnalyzerError):
    """GitHub service related errors"""
    pass

class BuildError(GitHubAnalyzerError):
    """Build process related errors"""
    pass

class AnalysisError(GitHubAnalyzerError):
    """Analysis related errors"""
    pass 