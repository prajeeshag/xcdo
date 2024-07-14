import hashlib
from .interfaces import ICacheHandler
import typing as t


class CacheHandler(ICacheHandler):

    def generate_hash(self, commands: t.Tuple[str, ...]) -> str:
        combined_string = " ".join(commands)
        hash_object = hashlib.sha256(combined_string.encode())
        hash_code = hash_object.hexdigest()
        return hash_code
