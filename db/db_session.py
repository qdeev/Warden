from typing import *
import sqlalchemy as sa
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import AutomapBase, automap_base

db = [r"db\databases\bot_serversettings.db"]
__engines: Dict[str, MockConnection] = dict()
databases: Dict[str, AutomapBase] = dict()
sessions: Dict[str, Session] = dict()


def global_init(db_files: List[str]):
    engines_init(db_files)

    names = list(__engines.keys())

    databases_init(names)
    sessions_init(names)


def engines_init(db_files: List[str]) -> None:
    global __engines

    if not db_files:
        raise NameError("No db files found")

    for db_file in db_files:
        database_name = f"sqlite:///{db_file}?check_same_thread=False"  # URI
        name = db_file.split("\\")[-1].split(".")[0]

        __engines[name] = sa.create_engine(database_name)


def databases_init(db_names: List[str]):
    global databases

    for name in db_names:
        metadata = sa.MetaData()
        metadata.reflect(__engines[name])

        databases[name] = automap_base(metadata=metadata)
        databases[name].prepare()
        databases[name].metadata.create_all(__engines[name])


def sessions_init(db_names: List[str]):
    global sessions

    for name in db_names:
        sessions[name] = Session(__engines[name])

