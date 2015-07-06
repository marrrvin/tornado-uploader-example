
# FileShare

## Структура проекта

* uploader - код приложения.
* static - статические файлы (css, javascript).
* templates - шаблоны
* uploaded - каталог по-умолчанию для загружаемых файлов

## Установка

Устанавливаем зависимости с помощью pip:

```python
pip install -r requirements.txt
```

## Запуск

Запускаем сервер:

```python
python2.7 ./uploader.py --port=8888
```

Приложение доступно по адресу: http://127.0.0.1:8888/

## Совместимость

Приложение протестировано на версиях питона:

* Python 2.7.6
* Python 3.4.0

В браузерах:

* Google Chrome Version 43.0.2357.130 (64-bit)
* Firefox 38.0

под управлением Ubuntu Linux 14.04
