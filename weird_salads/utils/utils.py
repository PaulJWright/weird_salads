import uuid

__all__ = ["generate_str_uuid"]


def generate_str_uuid():
    """str(uuid) for sqlite"""
    return str(uuid.uuid4())
