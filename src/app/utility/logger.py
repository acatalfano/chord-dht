import logging
from typing import Union
import verboselogs


class Logger:
    __instance: verboselogs.VerboseLogger = None

    @staticmethod
    def logger() -> verboselogs.VerboseLogger:
        if Logger.__instance is None:
            Logger()
        assert(Logger.__instance is not None)
        return Logger.__instance

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception('Tried to reinstantiate the singleton')
        else:
            Logger.__instance = verboselogs.VerboseLogger('verbose logger')
            Logger.__instance.addHandler(logging.StreamHandler())
