from typing import List, Dict
import db


def get_all() -> List[Dict]:
    db_conn = db.connect()
    books = db_conn.execute('select * from tbl_books')
    return [{**book} for book in books]


def book_exist(book_id: int) -> bool:
    db_conn = db.connect()
    exist = db_conn.execute(
        f"""
                    select 
                        1
                    from tbl_books r
                    where r.id =  {book_id}
        """
    ).fetchone()
    if exist:
        return True
    return False


def get_book(book_id: int) -> Dict:
    db_conn = db.connect()
    book = db_conn.execute(
        f"""
                    select 
                        *
                    from tbl_books r
                    where r.id =  {book_id}
        """
    ).fetchone()
    return {**book}
