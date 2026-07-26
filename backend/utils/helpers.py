"""
Utility Helper Functions
"""

import hashlib
import re
from urllib.parse import urlparse


def sha256(text: str):

    return hashlib.sha256(
        text.encode()
    ).hexdigest()


def normalize(text: str):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def valid_url(url: str):

    try:

        parsed = urlparse(url)

        return bool(
            parsed.scheme
            and parsed.netloc
        )

    except Exception:

        return False


def remove_duplicate_strings(items):

    seen = set()

    result = []

    for item in items:

        if item in seen:
            continue

        seen.add(item)

        result.append(item)

    return result


def cosine_similarity(a, b):

    import numpy as np

    a = np.array(a)

    b = np.array(b)

    return np.dot(a, b) / (
            np.linalg.norm(a)
            * np.linalg.norm(b)
    )