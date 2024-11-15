import bcrypt
from ..config import get_db_connection

def check_credentials(username):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetCredentials(%s); """, (username,))
            credentials = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return credentials

def get_all_users():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetActiveUsers(); """)
            users = cursor.fetchall() or []
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        users = []
    finally:
        db.close()

    return users

def get_user_by_id(user_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetUserDetails(%s); """, (user_id,))
            user = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        user = None
    finally:
        db.close()

    return user

def check_exists_user(user_ci):
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT ci FROM User WHERE ci = %s
            """, (user_ci,))
            result = cursor.fetchall()
            if result:
                ci = result[0]
                return ci
            else:
                return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()

def create_user(user):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            print(f"el ci es: {user.ci}")
            cursor.execute(
                """ 
                CALL InsertUser(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                """,
                (user.user_name, user.password, user.name, user.last_name, user.second_last_name,
                user.phone, user.email, user.address, user.birth_date, user.genre, user.ci, user.role_id)
            )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def update_user(user):
    db = get_db_connection()
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(
                """ CALL UpdateUserByID(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                (user.user_id, user.name, user.last_name, user.second_last_name,
                user.phone, user.email, user.address, user.birth_date, user.genre, user.ci, user.role_id)
            )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def delete_user(user_id):
    db = get_db_connection()
    try:
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL DeleteUser(%s) """, (user_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()