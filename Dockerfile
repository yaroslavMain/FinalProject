# указываем образ по умолчанию
FROM python:3.11.4

# выставляем рабочую директорию
WORKDIR /app

# копируем файл requirements из проекта в контейнер
COPY ./requirements.txt /app/requirements.txt

# указывает Python что не надо создавать кеш файлы с байт кодом pyc
ENV PYTHONDONTWRITEBYTECODE 1
# указываем Python что нет необходимости кешировать ввод/вывод
ENV PYTHONUNBUFFERED 1

# создание и активация окружения (преимущественно для Django)
# RUN python3 -m venv venv
# RUN source venv/bin/activate

# --no-cache-dir не создавать директорию с кешем, устанавливаем все зависимости
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# указываем необходимость открыть 8000 порт (не обязателен)
EXPOSE 8000

# копируем исходный код проекта
COPY . /app