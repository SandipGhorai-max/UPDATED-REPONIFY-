from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Cerebras API Keys (4 keys for rotation)
    CEREBRAS_API_KEY_1: str
    CEREBRAS_API_KEY_2: str
    CEREBRAS_API_KEY_3: str
    CEREBRAS_API_KEY_4: str

    # Cerebras Models — one per pipeline layer
    CEREBRAS_VISION_MODEL: str = "gpt-oss-120b"
    CEREBRAS_CREATIVE_MODEL: str = "gpt-oss-120b"

    # GitHub Tokens
    GITHUB_TOKEN_1: str
    GITHUB_TOKEN_2: str

    # Other existing settings
    GITHUB_API_BASE: str = "https://api.github.com"

    @property
    def cerebras_api_keys(self) -> list[str]:
        return [
            self.CEREBRAS_API_KEY_1,
            self.CEREBRAS_API_KEY_2,
            self.CEREBRAS_API_KEY_3,
            self.CEREBRAS_API_KEY_4,
        ]

    @property
    def github_tokens(self) -> list[str]:
        return [
            self.GITHUB_TOKEN_1,
            self.GITHUB_TOKEN_2,
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
