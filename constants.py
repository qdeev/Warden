import os
import logging
from db import db_session

db_session.global_init(db_session.db)
from db.db_session import sessions
from db.models import *

TOKEN_FILE = "TOKEN.txt"
with open(TOKEN_FILE) as tk:
    TOKEN = tk.readline()

PREFIX = "That's not a prefix it's just a sentence"
AUTHOR_ID = 290136163686285325

# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG, filename="log.txt", filemode='a')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
