from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Understand MS API"
    app_version: str = "1.0.0"

    cosmos_url: str = ""
    cosmos_database: str = "understand_ms"
    cosmos_conversations_container: str = "conversations"

    is_mock_response: bool = False
    mock_response_type: str = "success"

    model_config = {"env_file": [".env", ".env.local"], "env_file_encoding": "utf-8"}


settings = Settings()
