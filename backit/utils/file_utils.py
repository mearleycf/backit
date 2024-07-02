import os

def ensure_dir_exists(path):
    """Ensure that a directory exists at the given path, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        return True # Directory was created
    return False # Directory already existed