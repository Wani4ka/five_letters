import logging
import os

from storage import BaseStorage
from storage.in_memory import InMemoryStorage
from storage.mongo import MongoStorage

LOGGER = logging.getLogger(__name__)

environ_storage_mode = '5LETTERS_STORAGE_MODE'
environ_db_host = '5LETTERS_MONGO_DB_HOST'
environ_db_name = '5LETTERS_MONGO_DB_NAME'

def from_os_environ() -> BaseStorage:
    if environ_storage_mode not in os.environ or os.environ[environ_storage_mode] != 'mongodb':
        LOGGER.info("Using in-memory storage")
        from words import words
        return InMemoryStorage(words)

    LOGGER.info("Using mongodb storage")

    db_name = '5letters'
    if environ_db_name in os.environ:
        db_name = os.environ[environ_db_name]

    return MongoStorage(db_name, os.environ[environ_db_host])
