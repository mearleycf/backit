#!/usr/bin python3

import toml
from toml.decoder import TomlDecodeError
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class BackupConfig:
    """Data class to store backup configuration settings."""
    source_directories: List[str]
    exclude_directories: List[str]
    backup_directory: str
    number_of_copies_to_keep: int

@dataclass
class LoggingConfig:
    """Data class to store logging configuration settings."""
    log_directory: str
    archive_directory: str
    log_retention_period: str
    log_level: str
    color_setup: Dict[str, str, str, str, str]
    custom_levels: Dict[str, Dict[str, str, str, str, str]]

@dataclass
class GitConfig:
    """Data class to store Git configuration settings."""
    remote_repository: str
    default_branch: str
    remote_name: str

@dataclass
class CeleryConfig:
    """Data class to store Celery configuration settings."""
    broker_url: str
    result_backend: str
    frequency: str
    schedule: Dict[str, int]

@dataclass
class MiscConfig:
    """Data class to store miscellaneous configuration settings."""
    lock_file_location: str
    timeout_value: int

@dataclass
class GlobalConfig:
    """Data class to store all global configuration settings."""
    debug_mode: bool
    verbose_mode: bool
    backup: BackupConfig
    logging: LoggingConfig
    git: GitConfig
    celery: CeleryConfig
    misc: MiscConfig

class Config:
    """
    A class to manage and parse configuration settings from a TOML file.

    Args:
        config_path (str): The path to the configuration file.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If there are issues parsing the configuration file.
    """

    def __init__(self, config_path: str = "config.toml"):
        """
        Initialize the Config class and load the configuration data from a TOML file.

        :param config_path: The path to the configuration file.
        :type config_path: str

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If there are issues parsing the configuration file.
        """
        try:
            self.config_data = toml.load(config_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {config_path}")
        except TomlDecodeError:
            raise ValueError(f"Error parsing config file at {config_path}, it is malformed.")
        try:
            self.global_config = self._parse_config(self.config_data["global"])
        except KeyError:
            raise ValueError("Missing 'global' section in config file.")

    def _validate_config(self, config_section: Dict, expected_keys: List[str]) -> None:
        """
        Validate the presence of all required keys in a configuration section.
        Args:
            config_section (Dict): The configuration section to validate.
            expected_keys (List[str]): A list of keys expected to be in the configuration section.
        Raises:
            ValueError: If any expected keys are missing.
        """
        missing_keys = [key for key in expected_keys if key not in config_section]
        if missing_keys:
            raise ValueError(f"Missing keys in config: {missing_keys}")
        return None

    def _parse_config(self, config_section: Dict) -> GlobalConfig:
        """
        Parse the global configuration section and instantiate data classes.
        Args:
            config_section (Dict): The 'global' configuration section from the TOML file.
        Returns:
            GlobalConfig: An instance of the GlobalConfig dataclass with all configurations loaded.
        """
        expected_keys = ["debug_mode", "verbose_mode", "backup.defaults", "logging.defaults", "git.defaults", "celery.defaults", "misc.defaults"]
        self._validate_config(config_section, expected_keys)

        return GlobalConfig(
            debug_mode=config_section["debug_mode"],
            verbose_mode=config_section["verbose_mode"],
            backup=BackupConfig(**config_section["backup.defaults"]),
            logging=LoggingConfig(**config_section["logging.defaults"]),
            git=GitConfig(**config_section["git.defaults"]),
            celery=CeleryConfig(**config_section["celery.defaults"]),
            misc=MiscConfig(**config_section["misc.defaults"])
        )