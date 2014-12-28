# coding: utf-8
import warnings
from decimal import Decimal
from functools import reduce

from config_parser.enums import ConversionTypeEnum
from config_parser.exceptions import ConversionTypeError
from config_parser.loader.json_loader import JSONLoader
from config_parser.utils import _


__author__ = 'damirazo <me@damirazo.ru>'


class ConfigParser(object):
    u"""
    Парсер конфигурационных файлов в формате json
    """

    def __init__(self, file_path, loader=JSONLoader):
        self.file_path = file_path
        self.loader = loader(file_path)
        self.data = self.loader.data
        # Таблица соответствия типов конвертирования и конвертирующих функций
        self.conversion_table = {
            ConversionTypeEnum.INTEGER: int,
            ConversionTypeEnum.DECIMAL: Decimal,
            ConversionTypeEnum.BOOL: self._boolean_conversion_handler,
            ConversionTypeEnum.STRING: str,
        }

    def register_conversion_handler(self, name, handler):
        u"""
        Регистрация обработчика конвертирования

        :param name: Имя обработчика в таблице соответствия
        :param handler: Обработчик
        """
        if name in self.conversion_table:
            warnings.warn(_(
                u'Конвертирующий тип с именем {} уже '
                u'существует и будет перезатерт!'
            ).format(name))

        self.conversion_table[name] = handler

    def conversion_handler(self, name):
        u"""
        Возвращает обработчик конвертации с указанным именем

        :param name: Имя обработчика
        :return: callable
        """
        try:
            handler = self.conversion_table[name]
        except KeyError:
            raise KeyError(_(
                u'Конвертирующий тип с именем {} отсутствует '
                u'в таблице соответствия!'
            ).format(name))

        return handler

    def has_param(self, key):
        u"""
        Проверка существования параметра с указанным именем

        :param key: Имя параметра
        """
        return self.get(key) is not None

    def get(self, key, default=None):
        u"""
        Возвращает значение с указанным ключем

        Пример вызова:
        value = self.get('system.database.name')

        :param key: Имя параметра
        :param default: Значение, возвращаемое по умолчанию
        :return: mixed
        """
        segments = key.split('.')
        result = reduce(
            lambda dct, k: dct and dct.get(k) or None,
            segments, self.data)

        return result or default

    def get_converted(self, key, conversion_type, default=None):
        u"""
        Возвращает значение, приведенное к типу,
        соответствующему указанному типу из таблицы соответствия

        :param key: Имя параметра
        :param conversion_type: Имя обработчика конвертации
            из таблицы соответствия
        :param default: Значение по умолчанию
        :return: mixed
        """
        # В случае отсутствия параметра сразу возвращаем значение по умолчанию
        if not self.has_param(key):
            return default

        value = self.get(key, default=default)
        handler = self.conversion_handler(conversion_type)

        try:
            value = handler(value)
        except Exception as exc:
            raise ConversionTypeError(_(
                u'Произошла ошибка при попытке преобразования типа: {}'
            ).format(exc))

        return value

    def get_int(self, key, default=None):
        return self.get_converted(
            key, ConversionTypeEnum.INTEGER, default=default)

    def get_bool(self, key, default=None):
        return self.get_converted(
            key, ConversionTypeEnum.BOOL, default=default)

    # =========================================================================
    # Обработчики различных типов
    # =========================================================================

    @staticmethod
    def _boolean_conversion_handler(value):
        value = value.lower()
        if value in ('true', 'false'):
            return value == 'true'

        return bool(value)