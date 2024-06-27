#!/usr/bin python3

import toml
from toml.decoder import TomlDecodeError
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class BackupConfig:
    source_directories: List[str]
    exclude_directories: List[str]
    backup_directory: str
    number_of_copies_to_keep: int

@dataclass
class LoggingConfig:
    log_directory: str
    archive_directory: str
    color_setup: Dict[str, str]
    custom_levels: Dict[str, Dict[str, str]]

@dataclass
class GitConfig:
    remote_repository: str
    default_branch: str
    remote_name: str

@dataclass
class CeleryConfig:
    broker_url: str
    result_backend: str
    frequency: str
    schedule: Dict[str, int]

@dataclass
class MiscConfig:
    lock_file_location: str
    timeout_value: int

@dataclass
class GlobalConfig:
    debug_mode: bool
    verbose_mode: bool
    backup: BackupConfig
    logging: LoggingConfig
    git: GitConfig
    celery: CeleryConfig
    misc: MiscConfig

class Config: 
    def __init__(self, config_path="config.toml"):
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

    def _validate_config(self, config_section, expected_keys):
        missing_keys = [key for key in expected_keys if key not in config_section]
        if missing_keys:
            raise ValueError(f"Missing keys in config: {missing_keys}")

    def _parse_config(self, config_section):
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
    
    def get_backup_config(self, job_name=None):
        if job_name:
            job_config = self.config_data.get(f"backup.job.{job_name}.backup", {})
            return {**self.global_config.backup.__dict__, **job_config.get('backup', {})}
        return self.global_config.backup
    
    def get_logging_config(self, job_name=None):
        if job_name:
            job_config = self.config_data.get(f"backup.job.{job_name}.logging", {})
            return {**self.global_config.logging.__dict__, **job_config.get('logging', {})}
        return self.global_config.logging
    
    def get_git_config(self, job_name=None):
        if job_name:
            job_config = self.config_data.get(f"backup.job.{job_name}.git", {})
            return {**self.global_config.git.__dict__, **job_config.get('git', {})}
        return self.global_config.git

    def get_celery_config(self, job_name=None):
        if job_name:
            job_config = self.config_data.get(f"backup.job.{job_name}.celery", {})
            return {**self.global_config.celery.__dict__, **job_config.get('celery', {})}
        return self.global_config.celery
    
    def get_misc_config(self, job_name=None):
        if job_name:
            job_config = self.config_data.get(f"backup.job.{job_name}.misc", {})
            return {**self.global_config.misc.__dict__, **job_config.get('misc', {})}
        return self.global_config.misc
    
"""
example usage:
config = Config()
print(config.get_backup_config("fish_config")) # get specific job config
print(config.get_logging_config()) # get default logging config

# If you want to catch exceptions
try:
    config = Config()
except Exception as e:
    print(f"Failed to load configuration: {e}")
    # Appropriate error handling here, like exit the program or revert to defaults
"""