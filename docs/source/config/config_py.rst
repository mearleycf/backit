.. _config_module:

config module
=============

The ``config`` module is responsible for loading, parsing, and validating configuration settings from a TOML file. It utilizes Python's dataclasses to structure the configuration data effectively.

Classes
-------

.. dataclass:: BackupConfig
   :members:

   Manages backup-specific settings including source directories, directories to exclude, backup destination, and retention policies.

.. dataclass:: LoggingConfig
   :members:

   Configures logging details such as log directory, archive directory, color setup, and custom log levels.

.. dataclass:: GitConfig
   :members:

   Contains settings for Git operations like repository URL, default branch, and remote name.

.. dataclass:: CeleryConfig
   :members:

   Holds configuration for Celery tasks including broker URL, result backend, scheduling frequency, and specific schedule details.

.. dataclass:: MiscConfig
   :members:

   Miscellaneous settings including the location of the lock file and timeout values for operations.

.. dataclass:: GlobalConfig
   :members:

   Aggregates all global configurations that apply across different parts of the application. This includes debugging settings, verbosity, and configurations for backups, logging, Git, Celery, and miscellaneous settings.

Class Config
------------

.. autoclass:: Config
   :members:
   :show-inheritance:

   The ``Config`` class initializes by loading the TOML configuration file and parsing the global settings into respective configuration objects. It provides methods to retrieve configurations specific to different backup jobs as well as default configurations.

Functions
---------

.. autofunction:: _validate_config
   :private:

   Validates the presence of required keys in a configuration section.

.. autofunction:: _parse_config
   :private:

   Parses the global configuration section and initializes ``GlobalConfig`` dataclass.

Example Usage
-------------

Below is an example on how to use the ``Config`` class to access configuration settings:

.. code-block:: python

   # Initialize the configuration
   config = Config()

   # Get the default backup configuration
   print(config.get_backup_config())

   # Get the backup configuration for a specific job
   print(config.get_backup_config("<job_specific_name>"))

   # Handle exceptions on configuration load
   try:
       config = Config()
   except Exception as e:
       print(f"Failed to load configuration: {e}")
       # Appropriate error handling

Configuration File Format
-------------------------

The configuration settings are expected to be defined in a TOML file, which allows easy readability and editing. The structure of the TOML file is outlined below with explanations for each section:

.. code-block:: toml

   # Global default settings
   [global]
   debug_mode = false
   verbose_mode = true

   # Default backup settings
   [backup.defaults]
   source_directories = []
   exclude_directories = []
   backup_directory = "/path/to/your/backup/repository/directory"
   number_of_copies_to_keep = 2

   # Default logging settings
   [logging.defaults]
   log_directory = "/path/to/your/backup/logs/directory"
   archive_directory = "/path/to/your/backup/logs/archive/directory"
   color_setup = { info = "<fg #03edf9>", error = "<fg #fc28a8>" }
   custom_levels = { custom_msg = { no = 27, color = "<fg #4e00ff>", icon = "🚀" } }

   # Default Git settings
   [git.defaults]
   remote_repository = "https://github.com/your_username/your_backup_repository.git"
   default_branch = "main"
   remote_name = "origin"

   # Default Celery settings
   [celery.defaults]
   broker_url = "amqp://guest@localhost//"
   result_backend = "rpc://"
   frequency = "weekly"
   schedule = { day_of_week = 0, hour = 8, minute = 30 }

   # Additional miscellaneous settings
   [misc.defaults]
   lock_file_location = "/path/to/your/backup/repository/directory/locks/lockfile.lock"
   timeout_value = 120  # Timeout for processes in seconds

   # Job-specific backup settings for fish_config
   [backup.job.fish_config.backup]
   source_directories = []
   backup_directory = "/path/to/your/first/backup_job/repository/directory"
   
   [backup.job.fish_config.git]
   remote_repository = "https://github.com/your_username/your_job_backup_repository.git"

   [backup.job.fish_config.logging]
   log_directory = "/path/to/your/backup/logs/job_specific/directory"
   archive_directory = "/path/to/your/backup/logs/job_specific/archive/directory"

   [backup.job.fish_config.celery]
   frequency = "daily"
   schedule = { day_of_week = 0, hour = 8, minute = 30 }

Error Handling
--------------

The ``Config`` class is designed to handle various types of errors such as missing files, malformed TOML content, or missing configuration sections. Proper error handling ensures that the application provides clear error messages and allows for fallback mechanisms or graceful exits.

Summary
-------

This module plays a crucial role in the configuration management of the application, ensuring that settings are loaded correctly and are accessible throughout the application. It supports flexibility in configuration with defaults and overrides for specific jobs.