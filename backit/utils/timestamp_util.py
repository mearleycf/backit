import datetime
import uuid
from config import Config

def get_timestamp_format(for_logging=False):
    config = Config()
    if for_logging:
        return config.logging.timestamp or config.general_settings.timestamp or "%Y-%m-%d_%H-%M-%S"
    return config.global_settings.timestamp or "%Y-%m-%d_%H-%M-%S"

def create_timestamp(for_logging=False):
    """Generate a timestamp using the configured format, optionally for logging."""
    timestamp_format = get_timestamp_format(for_logging=for_logging)
    return datetime.datetime.now().strftime(timestamp_format)

def create_timestamp_with_uuid(for_logging=False):
    """Generate a timestamp appended with a UUID, optionally for logging."""
    timestamp = create_timestamp(for_logging=for_logging)
    unique_id = str(uuid.uuid4()).replace("-", "")
    return f"{timestamp}_{unique_id}"

# Example usage
if __name__ == "__main__":
    print("General Timestamp:", create_timestamp())
    print("Logging Timestamp:", create_timestamp(for_logging=True))
    print("General Timestamp with UUID:", create_timestamp_with_uuid())
    print("Logging Timestamp with UUID:", create_timestamp_with_uuid(for_logging=True))