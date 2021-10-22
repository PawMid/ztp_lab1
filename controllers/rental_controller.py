from typing import List, Dict
import db
import controllers.user_controller as user_controller


def user_rentals(user_id: int) -> List[Dict]:
    db_conn = db.connect()
    rentals = db_conn.execute(
        f"""
            select 
                    b.title, 
                    b.author, 
                    r.rental_date 
            from tbl_rentals r join tbl_books b on b.id = r.bookid_fk 
            where r.userid_fk =  {user_id}
"""
    ).fetchall()
    return [{**rent} for rent in rentals]


def user_has_rentals(user_id: int):
    db_conn = db.connect()
    rentals = db_conn.execute(
        f"""
                select 
                    1
                from tbl_rentals r
                where r.userid_fk =  {user_id}
    """
    ).fetchall()

    if len(rentals) > 0:
        return True
    return False


def count_rentals(book_id: int) -> int:
    db_conn = db.connect()
    rentals = db_conn.execute(
        f"""
                    select 
                        count(*) as cnt
                    from tbl_rentals r
                    where r.bookid_fk =  {book_id} and r.return_date is null
        """
    ).fetchone()
    return rentals[0]


def book_rented_by(book_id: int) -> List[Dict]:
    db_conn = db.connect()
    renters = []
    result = db_conn.execute(
        f"""
            select 
                r.id,
                r.rental_date,
                r.return_date,
                r.userid_fk
            from tbl_rentals r
            where r.bookid_fk =  {book_id}
        """
    ).fetchall()

    if result:
        for row in result:
            ud = {**row}
            # noinspection PyTypeChecker
            data = user_controller.by_id(ud['userid_fk'])
            ud['user'] = data
            ud.pop('userid_fk', None)
            renters.append(ud)
    return renters


def get_rental_obj_by_id(rental_id: int) -> Dict:
    db_conn = db.connect()
    result = db_conn.execute(
        f"""
                    select 
                        r.id,
                        r.rental_date,
                        r.return_date,
                        r.userid_fk
                    from tbl_rentals r
                    where  r.id = {rental_id}
                """
    ).fetchone()
    ud = {**result}
    # noinspection PyTypeChecker
    data = user_controller.by_id(ud['userid_fk'])
    ud['user'] = data
    ud.pop('userid_fk', None)
    return ud


def rent_book(book_id, user_id):
    db_conn = db.connect()
    db_conn.execute(
        f"""
            INSERT INTO 
        "tbl_rentals"("userid_fk", "bookid_fk", "rental_date", "return_date") 
        VALUES ({user_id}, {book_id}, date(), null);
        """
    ).fetchone()
    db_conn.commit()

    rent_id = db_conn.execute('select last_insert_rowid()').fetchone()

    return rent_id[0]


def return_book(book_id, user_id):
    db_conn = db.connect()
    return_id = db_conn.execute(f"""
                select t.id 
                from tbl_rentals t 
                where t.bookid_fk =  {book_id} 
                and t.userid_fk = {user_id} 
                and t.return_date is null 
                order by id ASC LIMIT 1
""").fetchone()[0]
    db_conn.execute(
        f"""
            update
            tbl_rentals 
            set return_date = date()
            where 
            bookid_fk = {book_id} 
            and userid_fk = {user_id} 
            and id = {return_id}
            """
    )
    db_conn.commit()
    return return_id


def is_rented_by_user(user_id: int, book_id: int) -> bool:
    db_conn = db.connect()
    result = db_conn.execute(
        f"""
                select 
                    1
                from tbl_rentals r
                where r.userid_fk =  {user_id} and r.bookid_fk = {book_id} and r.return_date is null
                """
    ).fetchall()

    if len(result) > 0:
        return True
    return False
