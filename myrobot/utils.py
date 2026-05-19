import os
import tempfile


def write_temp_file(content, suffix):
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(content)
        tmpfile = f.name
    return tmpfile


def check_and_delete(fpath):
    """
    Check if file exists and delete it
    """
    if os.path.exists(fpath):
        os.remove(fpath)
