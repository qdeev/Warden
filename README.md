Warden
=========================================================
Warden - это discord бот, большая часть функционала которого направлена на администрирование сервера.

Цель проекта: создать бота для discord средствами языка python, библиотеки discord.py и др.

Задачи:
•	реализовать функции администрирования сервера 
•	реализовать возможность настройки бота 
•	реализовать прослушивание музыки при помощи youtube_dl


Были созданы файлы, которые можно разбить на группы:
1. Основные файлы (main, constants)
	main: функции подключения, отключения и перезагрузки 	когов, 	запускает программу, инициализирует префикс сервера.
	constants: необходимые константы и инициализирует логгер

2. Коги (Bot, Entertainment, Settings)
	Bot: функции администрирования, а также функцию help
	Entertainment: функции для прослушивания музыки при помощи 	youtube_dl
	Settings: функции настройки сервера (каналы для логирования, mute 	роли, смена префикса и т. д.)

3. Файлы для работы с базой данных (db_session, models)
	db_session: инициализация соединения с базой данных
	models: инициализация ORM моделей
	
Для работы с discord серверами необходимо хранить данные о настройках, ролях, префиксах, каналах для каждого сервера, на котором есть Warden. С такой целью была создана база данных bot_serversettings.db, в ней все таблицы связаны при помощи id серверов, на которых есть бот, это позволяет хранить данные для каждого сервера. 
