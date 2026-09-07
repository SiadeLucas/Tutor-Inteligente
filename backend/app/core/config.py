"""
Configuração centralizada via variáveis de ambiente (Pydantic Settings).
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Banco de Dados ---
    DATABASE_URL: str = "postgresql+asyncpg://tutor_admin:senhalocal123@ti-database:5432/tutor_inteligente"

    # --- Redis ---
    REDIS_URL: str = "redis://:redislocal123@ti-redis:6379/0"

    # --- JWT ---
    JWT_SECRET_KEY: str = "chave_temporaria_dev_apenas_tutor_inteligente_2026"
    JWT_REFRESH_SECRET_KEY: str = "outra_chave_temporaria_dev_refresh_2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- IA ---
    GOOGLE_API_KEY: str = ""

    # --- Asaas ---
    ASAAS_API_KEY: str = ""
    ASAAS_WEBHOOK_SECRET_TOKEN: str = ""
    ASAAS_ENVIRONMENT: str = "sandbox"

    # --- AWS ---
    AWS_S3_BUCKET: str = "tutor-inteligente-assets"
    AWS_REGION: str = "sa-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""

    # --- Amazon SES ---
    SES_SENDER_EMAIL: str = "noreply@tutorinteligente.com.br"

    # --- Geral ---
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True
    )


settings = Settings()
