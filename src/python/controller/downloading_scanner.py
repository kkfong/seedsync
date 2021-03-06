# Copyright 2017, Inderpreet Singh, All rights reserved.

import logging
from typing import List
import multiprocessing
import queue

from .scanner_process import IScanner
from common import overrides
from system import SystemScanner, SystemScannerError, SystemFile


class DownloadingScanner(IScanner):
    """
    Scanner implementation to scan the downloading files only
    A caller sets the names of the downloading files that need to be scanned.
    A multiprocessing.Queue is used to store the names because the set and scan
    methods are called by different processes.
    """
    def __init__(self, local_path: str):
        self.__scanner = SystemScanner(local_path)
        self.__downloading_files_queue = multiprocessing.Queue()
        self.__downloading_files = []  # latest state
        self.logger = logging.getLogger("DownloadingScanner")

    @overrides(IScanner)
    def set_base_logger(self, base_logger: logging.Logger):
        self.logger = base_logger.getChild("DownloadingScanner")

    def set_downloading_files(self, file_names: List[str]):
        """
        Set the list of downloading files. Only these files will be scanned.
        :param file_names:
        :return:
        """
        self.__downloading_files_queue.put(file_names)

    @overrides(IScanner)
    def scan(self) -> List[SystemFile]:
        # Grab the latest list of downloading files, if any
        try:
            while True:
                self.__downloading_files = self.__downloading_files_queue.get(block=False)
        except queue.Empty:
            pass

        # Do the scan
        # self.logger.debug("Scanning files: {}".format(str(self.__downloading_files)))
        result = []
        for file_name in self.__downloading_files:
            try:
                result.append(self.__scanner.scan_single(file_name))
            except SystemScannerError as ex:
                # Ignore errors here, file may have been deleted
                self.logger.warning(str(ex))
        return result
