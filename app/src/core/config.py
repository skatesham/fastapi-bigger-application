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
    ROUTE_PREFIX_V1: str = "/v1"
    VERSION: str = Field(default="2.0.1")
    SERVICE_NAME: str = Field(default="fastapi-car-shop-erp")
    SERVICE_DESCRIPTION: str = Field(default="Professional ERP system for car shop management")
    SERVICE_AUTHOR: str = Field(default="Sham Vinicius Fiorin")
    
    # Security Configuration
    SECRET_KEY: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Database Configuration
    DATABASE_URL: str = Field(default="postgresql://skatesham:skatesham-github@localhost/skatesham")
    
    # CORS Configuration
    ALLOWED_HOSTS: Optional[str] = Field(default="*")
    
    # Environment Configuration
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="development")
    
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
ROUTE_PREFIX_V1 = settings.ROUTE_PREFIX_V1
VERSION = settings.VERSION
SERVICE_NAME = settings.SERVICE_NAME
SERVICE_DESCRIPTION = settings.SERVICE_DESCRIPTION
SERVICE_AUTHOR = settings.SERVICE_AUTHOR
ALLOWED_HOSTS = settings.allowed_hosts_list
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
DATABASE_URL = settings.DATABASE_URL
