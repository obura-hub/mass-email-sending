import touch
import os
import json


def get_default_settings() -> dict:
    return {
        "source_folder": touch.util.Settings.upload,
        "secure_folder": touch.util.Settings.upload_secure,
        "log_dir": touch.util.Settings.log_dir,
        "email": "touchkenyaemailer@gmail.com",
        "password": "@statement!",
        "default_password": "12345"
    }


def read_settings():
    try:
        with open(touch.util.Settings.config_file, "r") as f:
            settings = json.load(f)
            if validate_settings(settings):
                return settings
            else:
                touch.util.log.error("Corrupted settings file")
                return create_settings()
    except FileNotFoundError:
        touch.util.log.error("Settings file not found")
        return create_settings()
    except json.JSONDecodeError:
        touch.util.log.error("Corrupted settings file")
        return create_settings()
    except Exception as err:
        touch.util.log.fatal("Read settings error : {}".format(err), 103)


def validate_settings(settings: dict):
    touch.util.log.debug("Validating settings")
    default_settings = get_default_settings()
    for key in default_settings:
        if key not in settings:
            return False
        else:
            try:
                method = getattr(touch.util.loader, "validate_"+key)
            except Exception as err:
                method = None
            if method:
                method(settings.get(key))
    return True


def validate_source_folder(value):
    if not os.path.isdir(value):
        if not create_directory(value):
            touch.util.log.fatal("Failed to create required directory {}".format(value), 103)


def create_directory(directory) -> bool:
    try:
        touch.util.log.debug("Creating directory : {}".format(directory))
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as err:
        touch.util.log.debug("Error creating directory: {} -  {}".format(directory, err))
        return False


def validate_secure_folder(value):
    if not os.path.isdir(value):
        if not create_directory(value):
            touch.util.log.fatal("Failed to create required directory {}".format(value), 103)


def validate_log_dir(value) -> bool:
    if not os.path.isdir(value):
        if not create_directory(value):
            touch.util.log.fatal("Failed to create required directory {}".format(value), 103)


def create_settings() -> dict:
    touch.util.log.debug("Creating a default settings profile")
    try:
        with open(touch.util.Settings.config_file, "w") as f:
            settings = get_default_settings()
            json.dump(settings, f)
        return read_settings()
    except Exception as err:
        touch.util.log.fatal("create settings error : {}".format(err), 102)


def configure_settings() -> dict:
    config_dir = touch.util.Settings.config_dir
    touch.util.log.debug("Loading configurations : {}".format(config_dir))
    if os.path.isdir(config_dir):
        touch.util.log.debug("Parsing configuration directory")
        touch.util.Settings.settings = read_settings()
    else:
        touch.util.log.error("Configuration directory not found")
        if create_configuration():
            touch.util.Settings.settings = create_settings()
        else:
            touch.util.log.fatal("Configuration directory could not be setup", 101)


def create_configuration() -> bool:
    touch.util.log.debug("Creating configuration directory")
    try:
        os.makedirs(touch.util.Settings.config_dir, exist_ok=True)
        return True
    except Exception as err:
        touch.util.log.error("Create configuration directory error : {}".format(err))
        return False


def load_settings():
    configure_settings()
