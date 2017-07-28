# Copyright 2017, Inderpreet Singh, All rights reserved.

import logging
import sys
import unittest
from unittest.mock import MagicMock

from model import Model, ModelFile, IModelListener, ModelError


class DummyModelListener(IModelListener):
    def file_added(self, file: ModelFile):
        pass

    def file_removed(self, file: ModelFile):
        pass

    def file_updated(self, file: ModelFile):
        pass


class TestLftpModel(unittest.TestCase):
    logger = None

    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(cls.__name__)
        handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        TestLftpModel.logger = logger

    def test_add_file(self):
        model = Model(logger=self.logger)
        file = ModelFile("test")
        model.add_file(file)
        recv_file = model.get_file("test")
        self.assertEqual("test", recv_file.name)

    def test_get_unknown_file(self):
        model = Model(logger=self.logger)
        with self.assertRaises(ModelError):
            model.get_file("test")

    def test_remove_file(self):
        model = Model(logger=self.logger)
        file = ModelFile("test")
        model.add_file(file)
        model.remove_file(file)
        with self.assertRaises(ModelError):
            model.get_file("test")

    def test_remove_unknown_file(self):
        model = Model(logger=self.logger)
        file = ModelFile("test")
        with self.assertRaises(ModelError):
            model.remove_file(file)

    def test_update_file(self):
        model = Model(logger=self.logger)
        file = ModelFile("test")
        file.local_size = 100
        model.add_file(file)
        recv_file = model.get_file("test")
        self.assertEqual(100, recv_file.local_size)
        recv_file.local_size = 200
        model.update_file(recv_file)
        recv_file = model.get_file("test")
        self.assertEqual(200, recv_file.local_size)

    def test_update_unknown_file(self):
        model = Model(logger=self.logger)
        file = ModelFile("test")
        with self.assertRaises(ModelError):
            model.update_file(file)

    def test_update_local_copy(self):
        model = Model(logger=self.logger)
        file = ModelFile("test")
        file.local_size = 100
        model.add_file(file)
        file.local_size = 200
        recv_file = model.get_file("test")
        # local update should not be reflected in the model
        self.assertEqual(100, recv_file.local_size)

    def test_add_listener(self):
        model = Model(logger=self.logger)
        listener = DummyModelListener()
        model.add_listener(listener)

    def test_listener_file_added(self):
        model = Model(logger=self.logger)
        listener = DummyModelListener()
        model.add_listener(listener)

        listener.file_added = MagicMock()

        file = ModelFile("test")
        model.add_file(file)
        # noinspection PyUnresolvedReferences
        listener.file_added.assert_called_once_with(file)

    def test_listener_file_removed(self):
        model = Model(logger=self.logger)
        listener = DummyModelListener()
        model.add_listener(listener)

        listener.file_removed = MagicMock()

        file = ModelFile("test")
        model.add_file(file)
        model.remove_file(file)
        # noinspection PyUnresolvedReferences
        listener.file_removed.assert_called_once_with(file)

    def test_listener_file_updated(self):
        model = Model(logger=self.logger)
        listener = DummyModelListener()
        model.add_listener(listener)

        listener.file_updated = MagicMock()

        file = ModelFile("test")
        file.local_size = 100
        model.add_file(file)
        file.local_size = 200
        model.update_file(file)
        # noinspection PyUnresolvedReferences
        listener.file_updated.assert_called_once_with(file)

    def test_listener_receives_copies(self):
        model = Model(logger=self.logger)
        listener = DummyModelListener()
        model.add_listener(listener)

        def side_effect(rx_file: ModelFile):
            rx_file.local_size = 200

        listener.file_added = MagicMock()
        listener.file_added.side_effect = side_effect
        listener.file_updated = MagicMock()
        listener.file_updated.side_effect = side_effect

        file = ModelFile("test")
        file.local_size = 100

        # below we check that the side effect is not reflected in the
        # file received from the get_file method

        model.add_file(file)
        # noinspection PyUnresolvedReferences
        self.assertEqual(1, listener.file_added.call_count)
        recv_file = model.get_file("test")
        self.assertEqual(100, recv_file.local_size)

        model.update_file(file)
        # noinspection PyUnresolvedReferences
        self.assertEqual(1, listener.file_updated.call_count)
        recv_file = model.get_file("test")
        self.assertEqual(100, recv_file.local_size)