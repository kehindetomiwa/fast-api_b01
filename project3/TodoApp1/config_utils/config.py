from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """"
    setting of Todo App
    All the below variables can be overridden by environment variables *case insensitive*
    """
    db_url: str = "postgresql://postgres:test1234!@localhost/TodoAppDB"
    #db_url = "sqlite:///./todosapp.db"

def get_config():
    return Settings()