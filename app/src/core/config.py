from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using Pydantic Settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # API Configuration
    API_PREFIX: str = "/api"
    JWT_TOKEN_PREFIX: str = "Authorization"
    ROUTE_PREFIX_V1: str = "/v1"
    
    # Security Configuration
    SECRET_KEY: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = Field(default="HS256")
    
    # Database Configuration
    DATABASE_URL: str = Field(default="postgresql://skatesham:skatesham-github@localhost/skatesham")
    
    # CORS Configuration
    ALLOWED_HOSTS: Optional[str] = Field(default="*")
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        """Convert comma-separated hosts to list"""
        if not self.ALLOWED_HOSTS or self.ALLOWED_HOSTS == "*":
            return ["*"]
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",") if host.strip()]


# Global settings instance
settings = Settings()

# Export constants for backward compatibility
API_PREFIX = settings.API_PREFIX
JWT_TOKEN_PREFIX = settings.JWT_TOKEN_PREFIX
ROUTE_PREFIX_V1 = settings.ROUTE_PREFIX_V1
ALLOWED_HOSTS = settings.allowed_hosts_list
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
DATABASE_URL = settings.DATABASE_URL
