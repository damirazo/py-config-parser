Парсер конфигурационных файлов для приложений на Python
=======================================================

Примеры использования:
----------------------

config.py


```
from config_parser.parser import ConfigParser


parser = ConfigParser(file_path='/path/to/config.json')

DEBUG = parser.get_bool('system.debug', False)
ALLOWED_HOSTS = parser.get('system.allowed_hosts', ())
```


config.json

```
{
    "system": {
        "debug": "true",
        "allowed_hosts": [
            '127.0.0.1'
        ]
    }
}
```