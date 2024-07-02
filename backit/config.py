#!/usr/bin python3

import toml
from toml.decoder import TomlDecodeError
from dataclasses import dataclass, field
from typing import Dict, List

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
    log_prefix: str
    log_retention_period: str
    log_level: str
    timestamp: str
    log_format: str
    color_setup: List[Dict[str, str]]
    custom_levels: Dict[str, Dict[str, str]]

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
class GeneralConfig:
    """Data class to store all global configuration settings."""
    debug_mode: bool
    verbose_mode: bool
    timestamp: str
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
        
        self.general_config = self._parse_general_config()
        self.backup_config = self._parse_backup_config()
        self.logging_config = self._parse_logging_config()
        self.git_config = self._parse_git_config()
        self.celery_config = self._parse_celery_config()
        self.misc_config = self._parse_misc_config()

    def _parse_general_config(self) -> GeneralConfig:
        config_section = self.config_data.get("general_settings", {})
        return GeneralConfig(
            debug_mode=config_section.get("debug_mode", False),
            verbose_mode=config_section.get("verbose_mode", True),
            timestamp=config_section.get("timestamp", "%Y-%m-%d %H:%M:%S")
        )

    def _parse_backup_config(self) -> BackupConfig:
        config_section = self.config_data.get("backup.defaults", {})
        return BackupConfig(
            source_directories=config_section.get("source_directories", []),
            exclude_directories=config_section.get("exclude_directories", []),
            backup_directory=config_section.get("backup_directory", ""),
            number_of_copies_to_keep=config_section.get("number_of_copies_to_keep", 0)
        )

    def _parse_logging_config(self) -> LoggingConfig:
        config_section = self.config_data.get("logging.defaults", {})
        return LoggingConfig(
            log_directory=config_section.get("log_directory", ""),
            archive_directory=config_section.get("archive_directory", ""),
            log_prefix=config_section.get("log_prefix", ""),
            log_retention_period=config_section.get("log_retention_period", ""),
            log_level=config_section.get("log_level", "INFO"),
            timestamp=config_section.get("timestamp", "%Y-%m-%d %H:%M:%S"),
            log_format=config_section.get("log_format", ""),
            color_setup=config_section.get("color_setup", []),
            custom_levels=config_section.get("custom_levels", {})
        )

    def _parse_git_config(self) -> GitConfig:
        config_section = self.config_data.get("git.defaults", {})
        return GitConfig(
            remote_repository=config_section.get("remote_repository", ""),
            default_branch=config_section.get("default_branch", "main"),
            remote_name=config_section.get("remote_name", "origin")
        )

    def _parse_celery_config(self) -> CeleryConfig:
        config_section = self.config_data.get("celery.defaults", {})
        return CeleryConfig(
            broker_url=config_section.get("broker_url", ""),
            result_backend=config_section.get("result_backend", ""),
            frequency=config_section.get("frequency", ""),
            schedule=config_section.get("schedule", {})
        )

    def _parse_misc_config(self) -> MiscConfig:
        config_section = self.config_data.get("misc.defaults", {})
        return MiscConfig(
            lock_file_location=config_section.get("lock_file_location", ""),
            timeout_value=config_section.get("timeout_value", 120)
        )
