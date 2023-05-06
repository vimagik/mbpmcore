# MicroBPM core
## Установка
1. Запускаем docker compose
```bash
docker compose up -d
```
Активными будут все контейреры кроме Camunda.

2. Добавляем бд для Camunda
- подключаемся к базе
```bash
docker compose exec db psql -d django_db -U camunda -W
```
- вводим пароль от базы
- создаем еще одну бд
```bash
create database camunda owner camunda;
```

3. Запускаем конейнер с Camunda
```bash
docker compose start
```

4. Производим первоначальную настройку CMS
```
docker compose exec cms python manage.py makemigrations
docker compose exec cms python manage.py migrate
docker compose exec cms python manage.py collectstatic
docker compose exec cms python manage.py createsuperuser
```

5. Публикуем процесс "Непрерывный менеджмент" из моделлера
6. Регистрируем процесс в CMS
- заходим в админку и добавляем в core/process

|Name_ru|Name_en|Camunda_ID|Code|
|-------|-------|----------|----|
|Непрерывный менеджмент|Continius management|Process_0rlunnd|cm|
|Проведение встречи|Conducting the meeting|-|meet|

**Вуаля. Все готово!**
