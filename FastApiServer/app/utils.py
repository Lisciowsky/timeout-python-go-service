import logging
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
logger = logging.getLogger()


STATUS_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}

sent_messages = []


def log_message(message: str, level: str = "INFO", prevent_duplicates: bool = True):
    if prevent_duplicates:
        if message not in sent_messages:
            logger.log(msg=message, level=STATUS_LEVELS[level])

    logger.log(msg=message, level=STATUS_LEVELS[level])


class ThreadWithReturnValue(Thread):
    def __init__(
        self,
        timeout: int,
        group=None,
        target=None,
        name=None,
        args=(),
        kwargs={},
        Verbose=None,
    ):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self.timeout = timeout

    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, timeout=self.timeout)
        return self._return
