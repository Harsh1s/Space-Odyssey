def generate_uuid() -> str:
    from uuid import uuid4

    return str(uuid4())


def hasher(text: str) -> str:
    from hashlib import sha256

    """
    Takes a UTF-8 encoded piece of text of any length, and returns the SHA-256 hash of the text as a string object, in uppercase.
    """
    return sha256(bytes(text, "utf-8")).hexdigest().upper()
