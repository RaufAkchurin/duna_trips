1) Можно сделать систему регистрации и персонализации выдачи билетов
2) Сделать несколько видов выдачи билетов:
        a) СПециальные предлоожения из п.А
        б) Самые выгодные из А в Б
        в) ...
        и чередовать выдачу каждый раз
        ТАК ЖЕ сделать кнопки для каждого вида выдачи - чтобы принудительно запросить какой либо имеющийся

gunicorn -c gunicorn_config.py trip_admin.wsgi:application
gunicorn trip_admin.wsgi:application


                                        ДЕПЛОЙ V2

                    Deploy  
1) Подключаемся к серверу ssh root@555.444.666.777
2) Пароль от рута в СИРЭЭМКЕ
3) Добавляем на серва свой ссаш ключь чтобы каждый раз не вводить пароль
Чтобы прокинуть ключ выполните в терминале на Вашем устройстве команду

ssh-keygen -t rsa

Нажимаем enter, пока ключ не будет сгенерирован. Пробрасываем его на VPS

ssh-copy-id -i ~/.ssh/id_rsa.pub root@512.3512.8218.3215 

Вводим свой пароль от root.

4) Клонируем репозиторий https://github.com/RaufAkchurin/worker

5) Создаём виртуальную среду

6) Запускаем её, накатываем все зависимости

4) Создаём .env и копируем туда данные свои
**ВНМИАНИЕ!!!**
-на серваке LOCALHOST_IP в .env указываем АЙПИ сервера
-на локальном компе указываем 127.0.0.1:8000

5) В settings.py проверяем наличие обоих АЙПИ **ALLOWED_HOSTS = ['rting-erp.ru', 'айпи сервера', '127.0.0.1']**

5.1) копируем gunicorn_config.py в папку с manage.py

5.2) копируем passanger_wsgi.py в папку с manage.py

6) Запускаем джангу вот так 
**nohup python3 manage.py runserver 555.444.666.777:8000**
те при запуске надо указать настоящий айпи сервера

После закрытия терминала процесс будет жить, чтобы его найти в 
дальнейшем можно воспользоваться
**`ps aux | grep 'python3'`**

или так после настройки гуникорна

gunicorn -c gunicorn_config.py trip_admin.wsgi:application - из папки с manage.py
gunicorn trip_admin.wsgi:application - из папки с manage.py

8) чтобы завершить принудительно процесс, используй
**`kill -9 PID`**
Замените PID на фактический идентификатор процесса.



НАСТРОЙКА ГУНИКОРНА ЧТОБЫ РАБОТАЛ ЧЕРЕЗ ДОМЕН МНЕСТО АПИ

sudo apt update
sudo apt install nginx


создаём /etc/nginx/sites-available/myproject

добавляем  конфиг

server {
    listen 80;
    server_name 54.335.848.235 выф.ru;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static {
        alias /root/duna_trips/trip_admin/static;              # слеш не ставим
    }

    location /media/ {
        root /root/duna_trips/trip_admin;                       # media не пишем, слеш не ставим
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}


**ЗАПУСКАТЬ ГУНИКОРН ТОЛЬКО НА 0.0.0.0:8000 иначе бот не сможет слать запросы внутрь джанги!**

запуск              gunicorn -c gunicorn_config.py trip_admin.wsgi:application
остановка           pkill gunicorn
поиск               ps aux | grep 'gunicorn'

ЛОГИ НГИНКС         cat /var/log/nginx/error.log
Конфиг НГИНКС       sudo nano /etc/nginx/sites-available/myproject
Рестарт нгинкс      sudo service nginx restart



                        NGINX

/etc/nginx/nginx.conf

user root;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	types_hash_max_size 2048;
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_buffers 16 8k;
	# gzip_http_version 1.1;
	# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}


                КОМАНДЫ ОБЪЯЗАТЕЛЬНО ОБЕ ПОСЛЕ ВСЕХ НАСТРОЕК НГИНС И ГУНИКОРНА!!!
Чтобы сайт начал работать, Вам нужно настроить симлинк на файл /etc/nginx/sites-available/myproject из папки /etc/nginx/sites-enabled/:
 1) ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/
 2) рестарт sudo service nginx restart
 3) gunicorn -c gunicorn_config.py trip_admin.wsgi:application
 

    


         _НАСТРОЙКА АВТОМАТИЧЕСКОГО РЕСТАРТА В СЛУЧАЕ ПАДЕНИЯ_


        НАСТРОЙКА systemctl (автоматический перезапуск в случае падения)

**Создайте  2 файла службы(для джанго и для бота отдельно):**
sudo nano /etc/systemd/system/django.service
sudo nano /etc/systemd/system/bot.service


**Добавьте следующие конфигурациюи в файлы службы:**
[Unit]
Description=Django
After=network.target
Requires=django.service
PartOf=bot.service

[Service]
Type=simple
WorkingDirectory=/root/duna_trips/trip_admin
ExecStart=/root/duna_trips/my_venv/bin/gunicorn -c gunicorn_config.py trip_admin.wsgi:application
KillMode=process
Restart=always
RestartSec=10
EnvironmentFile=/root/duna_trips/.env

[Install]
WantedBy=multi-user.target



№2
[Unit]
Description=bot
After=network.target
Requires=django.service
PartOf=django.service

[Service]
Type=simple
WorkingDirectory=/root/duna_trips
ExecStart=/root/duna_trips/my_venv/bin/python3 /root/duna_trips/telegram/bot.py
KillMode=process
Restart=always
RestartSec=10
EnvironmentFile=/root/duna_trips/.env

[Install]
WantedBy=multi-user.target


            **ПОСЛЕ ПАРВОК В КОНФИГЕ**
sudo systemctl daemon-reload

sudo systemctl stop django
sudo systemctl stop bot

sudo systemctl start django
sudo systemctl start bot

systemctl status django.service
systemctl status bot.service

если что то неработает проверяем логи вот так

journalctl -u django.service
journalctl -u bot.service


      АВТОМАТИЧЕСКИЙ ПУШИНГ БАЗЫ НА ГИТХАБ НАСТРОЙКА

1) в .енв добавить токен от гитхаба
2) Для того чтобы скрипт выполнялся раз в день автоматически, вы можете использовать планировщик задач в операционной системе. Например, для Unix-подобных систем (Linux, macOS) это может быть cron.

Вот пример того, как вы можете настроить cron-задачу:

Откройте терминал.

Введите команду:

`crontab -e`
В редакторе cron-задач добавьте строку, которая будет запускать ваш скрипт раз в день. Например:

`0 13 * * * /root/worker/venv/bin/python3 /root/worker/bd_auto_push.py`
Эта строка означает, что скрипт будет запускаться каждый день в (13 часов, 0 минут). Вы можете изменить время запуска, используя другие значения.

Сохраните изменения и закройте редактор.
Таким образом, ваш скрипт будет выполняться ежедневно по заданному расписанию. Убедитесь, что пути к интерпретатору Python (python3) и вашему скрипту (bd_auto_push.py) указаны правильно в команде cron.


               



Статьи использовал
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#creating-systemd-socket-and-service-files-for-gunicorn

Решение вопроса со статик файлами (надо добавить рута в конфиге)
НО конфиг из РИДМИ уже готовый с рутом.
https://stackoverflow.com/questions/25774999/nginx-stat-failed-13-permission-denied/70142668#70142668






