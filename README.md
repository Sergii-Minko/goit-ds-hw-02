goit-ds-hw-01

# Створення віртуального середовища з використанням venv

python -m venv venv

# Активація віртуального середовища

source venv/Scripts/activate

# Встановлення Poetry

pip install poetry

# Перевірка версії Poetry

poetry --version

# Ініціалізація проекту

poetry init

# Встановлення залежностей

poetry install

# Активація віртуального середовища Poetry

poetry shell

# Оновлення залежностей

poetry update

# У редакторі коду створіть файли

requirements.txt

# Додайтє пакети у файл requirements.txt

python -m pip freeze > requirements.txt

# У редакторі коду створіть файли

Dockerfile

# Збірка Docker-образу

docker build . -t sergiiminko/goit-ds-hw-01

# Запуск контейнера в інтерактивному режимі

docker run -it sergiiminko/goit-ds-hw-01-2
