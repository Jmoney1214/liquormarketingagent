from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()
@dataclass
class Settings:
    model: str = os.getenv('MODEL','gpt-4.1')
    openai_api_key: str | None = os.getenv('OPENAI_API_KEY')
settings = Settings()
