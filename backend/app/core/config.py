from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KMA_", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/kma"
    redis_url: str = "redis://localhost:6379/0"
    event_backpressure_limit_per_minute: int = 1000
    finding_cooldown_minutes: int = 30
    pending_pod_threshold_minutes: int = 5
    crash_loop_restart_threshold_10m: int = 5
    resource_pressure_cpu_threshold: float = 0.85
    resource_pressure_memory_threshold: float = 0.90


settings = Settings()
