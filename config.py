from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    secret: str = "my-secret"
    db_uri: str = "mysql+mysqlconnector://root:1234@127.0.0.1:3306/myapp"


Config = Settings()
