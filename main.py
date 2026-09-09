from etl.config.settings import get_settings

settings = get_settings()

print(f"Database URL : {settings.database_url}")
