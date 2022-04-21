from constants import *
from db.db_session import databases

database = databases["bot_serversettings"].classes

Servers = database.servers
Prefix = database.prefix
Channels = database.channels
Roles = database.roles