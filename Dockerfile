# Docker-команда FROM вказує базовий образ контейнера
FROM python:3.12.2

# Встановимо змінну середовища
ENV APP_HOME /app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Install Poetry
RUN pip install 'poetry==1.8.2'

# Copy dependency files
# COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install

# Встановимо залежності всередині контейнера
RUN pip install -r requirements.txt

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 5000

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "./py/main.py"]