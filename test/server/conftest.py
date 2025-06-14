import logging
import os
import signal
import subprocess
from time import sleep

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def run_server_for_tests():
    if 'RUN_BUNDLED_SERVER' not in os.environ:
        yield False
        return None

    LOGGER.info("Starting server for tests")
    process = subprocess.Popen(["coverage", "run", "server.py"])
    sleep(0.5)
    yield True
    process.send_signal(signal.SIGINT)
    process.wait()
    LOGGER.info("Stopping server for tests")
    return None
