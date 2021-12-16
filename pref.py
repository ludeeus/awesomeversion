import time

from awesomeversion import AwesomeVersion
from packaging import version


class Timer:
    def __init__(self, name):
        self._start_time = None
        self._name = name

    def start(self):
        """Start a new timer"""
        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"[{self._name}] Elapsed time: {elapsed_time:0.4f} seconds")


timer = Timer("AwesomeVersion")
timer.start()
for x in range(1, 1000):
    AwesomeVersion(x) > AwesomeVersion("1")
timer.stop()


timer = Timer("packaging.version")
timer.start()
for x in range(1, 1000):
    version.parse(str(x)) > version.parse("1")
timer.stop()
