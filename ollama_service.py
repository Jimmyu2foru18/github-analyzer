import httpx
from logger import setup_logger
from config import Config

class OllamaServiceError(Exception):
    """Base exception for Ollama service errors"""
    pass

class OllamaService:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, log_dir=config.LOG_DIRECTORY)
        self.base_url = config.OLLAMA_BASE_URL.rstrip("/")

    async def generate(self, prompt: str, model: str = None) -> str:
        """Send a prompt to Ollama and get a response."""
        model = model or self.config.OLLAMA_MODEL
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                response.raise_for_status()
                return response.json().get("response", "")
        except httpx.HTTPError as e:
            self.logger.error(f"Ollama API request failed: {e}")
            raise OllamaServiceError(f"Ollama request failed: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in Ollama service: {e}")
            raise OllamaServiceError(f"Ollama service error: {e}")
