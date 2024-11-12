from ..config import get_db_connection

def get_all_smarts():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetActiveSmarts(); """)
            smarts = cursor.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        smarts = []
    finally:
        db.close()
    return smarts

def get_smart_by_id(smart_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetSmartById(%s); """, (smart_id,))
            smart = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        smart = None
    finally:
        db.close()

    return smart

def check_exists_smart(smart_rfid):
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT codeRFID FROM Smart WHERE codeRFID  = %s
            """, (smart_rfid,))
            result = cursor.fetchall()
            if result:
                smart_rfid = result[0]
                return smart_rfid
            else:
                return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()

def create_smart(smart):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                INSERT INTO Smart (codeRFID)
                VALUES (%s) 
                """,(smart.code_rfid,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def assignment_smart(smart):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                UPDATE Smart 
                SET idUser = %s, lastUpdate = CURRENT_TIMESTAMP
                WHERE status = 1 AND idSmart = %s; 
                """,(smart.user_id, smart.smart_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def update_smart(smart):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                UPDATE Smart
                SET codeRFID = %s, idUser = %s, available = %s,lastUpdate = CURRENT_TIMESTAMP
                WHERE idSmart = %s AND status = 1;
                """,(smart.code_rfid, smart.user_id, smart.available,smart.smart_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def delete_smart(smart_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                    UPDATE Smart
                    SET status = 0, lastUpdate = CURRENT_TIMESTAMP
                    WHERE idSmart = %s AND status = 1
                    """,(smart_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()
