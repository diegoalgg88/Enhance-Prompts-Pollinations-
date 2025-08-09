import configparser
from pathlib import Path
import logging

class ConfigManager:
    """Manages the application's configuration with secure default values."""

    def __init__(self, config_file: str = "config.ini") -> None:
        self.config_file: Path = Path(config_file)
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.load_config()

    def load_config(self) -> None:
        """Loads the configuration from the config file, or creates a default config if it doesn't exist."""
        if self.config_file.exists():
            try:
                self.config.read(self.config_file, encoding='utf-8')
            except Exception as e:
                logging.error(f"Error loading config: {e}")
                self._create_default_config()
        else:
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Creates a default configuration file with predefined settings."""
        self.config['API'] = {'base_url': 'https://text.pollinations.ai',
                              'endpoint': '/openai', 'timeout': '30', 'max_retries': '3'}
        self.config['APP'] = {
            'window_width': '900', 'window_height': '700', 'theme': 'native', 'max_history': '100'}
        self.config['SECURITY'] = {'validate_ssl': 'true', 'rate_limit': '10'}
        self.save_config()

    def save_config(self) -> None:
        """Saves the current configuration to the config file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            logging.error(f"Error saving config: {e}")

    def get(self, section: str, key: str, fallback: str = "") -> str:
        """Gets a string value from the config."""
        return self.config.get(section, key, fallback=fallback)

    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        """Gets an integer value from the config."""
        return self.config.getint(section, key, fallback=fallback)

    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Gets a boolean value from the config."""
        return self.config.getboolean(section, key, fallback=fallback)
