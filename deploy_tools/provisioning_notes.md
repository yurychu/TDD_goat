Инициализцация

## Требуемые пакеты

*nginx
*python 3
*git
*pip
*virtualenv

Ubuntu:

	sudo apt-get install nginx git python3 python3-pip
	sudo pip3 install virtualenv

## Nginx Virtual Host config

*смотреть nginx.template.conf
*заменить SITENAME на ваш, например staging.my-domain.com

## Upstart Job

*смотреть gunicorn-upstart.template.conf
*заменить SITENAME 

## Дерево каталогов
sites
	SITENAME
		database
		source
		static
		virtualenv

