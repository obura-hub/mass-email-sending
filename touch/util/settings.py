from . import loader
from . import  users
import os


class Settings:
    settings: dict
    users: dict
    home: str
    config_dir: str
    config_file: str
    upload: str
    upload_secure: str
    log_dir: str

    @staticmethod
    def load_settings():
        loader.load_settings()
        Settings.users = users.get_users()

    @staticmethod
    def get_setting(name: str) -> object:
        return Settings.settings.get(name, None)

    @staticmethod
    def get_user(_id: int) -> dict:
        user = Settings.users.get(_id, {})
        if user:
            user['id'] = _id
            return user
        return {}

    @staticmethod
    def set_home(home):
        Settings.home = home
        Settings.config_dir = home + os.path.sep + "config" + os.path.sep
        Settings.config_file = Settings.config_dir + "settings.json"
        Settings.upload = home + os.path.sep + "upload"
        Settings.upload_secure = home + os.path.sep  +"upload-secure"
        Settings.log_dir = home + os.path.sep + "log"
