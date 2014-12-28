# coding: utf-8
import json

__author__ = 'damirazo <me@damirazo.ru>'


class JSONLoader(object):
    u"""
    Загрузчик конфигурационного файла в формате JSON
    """

    def __init__(self, file_path):
        u"""
        :param basestring file_path: Путь до файла
        """
        self._data = None
        self.file_path = file_path
        self.file_descriptor = open(self.file_path)

    @property
    def data(self):
        if self._data is None:
            self._data = json.load(self.file_descriptor)

        return self._data