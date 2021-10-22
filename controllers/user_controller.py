from typing import List, Dict
import db


def get_all() -> List:
    db_conn = db.connect()
    users = db_conn.execute("select * from tbl_users").fetchall()
    parsed = [{**row} for row in users]
    return parsed


def exist(**kwargs) -> bool:
    if kwargs.get('name'):
        sql = f"select * from tbl_users where name = '{kwargs.get('name')}'"
    elif kwargs.get('id'):
        sql = f"select * from tbl_users where id = '{kwargs.get('id')}'"
    else:
        return False
    db_conn = db.connect()
    user = db_conn.execute(sql).fetchall()
    if len(user) > 0:
        return True
    return False


def by_name(name: str) -> Dict:
    db_conn = db.connect()
    user = db_conn.execute(f"select * from tbl_users where name = '{name}'").fetchone()
    return {**user}


def by_id(user_id: int) -> Dict:
    db_conn = db.connect()
    user = db_conn.execute(f"select * from tbl_users where id = {user_id}").fetchone()
    return {**user}


def add(name: str):
    db_conn = db.connect()
    db_conn.execute(f"insert into tbl_users(name) values ('{name}')")
    db_conn.commit()


def delete(user_id: int):
    db_conn = db.connect()
    db_conn.execute(f"delete from tbl_users where id = {user_id}")
    db_conn.commit()
