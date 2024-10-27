from ..config import get_db_connection

def get_all_balances():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT idBalance, balanceCode, IFNULL(actuallyFactor, 0.0) AS actuallyFactor, registerDate, IFNULL(lastUpdate, 'Sin Cambios') AS lastUpdate, available 
                FROM balance
                WHERE status = 1
                """)
    balances = cursor.fetchall()
    cursor.close()
    db.close()
    return balances

def get_balance_by_id(balance_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT idBalance, balanceCode, IFNULL(actuallyFactor, 0.0) AS actuallyFactor, registerDate, IFNULL(lastUpdate, 'Sin Cambios') AS lastUpdate, available 
                FROM balance
                WHERE status = 1 AND idBalance = %s
                """,(balance_id,))
    balance = cursor.fetchone()
    cursor.close()
    db.close()
    return balance

def create_balance(balance_code, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                INSERT INTO Balance (balanceCode, userID)
                VALUES (%s,%s) 
                """,(balance_code,user_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un Error:{e}")
        return False
    finally:
        cursor.close()
        db.close()
    return True

def update_balance(balance_id, balance_code, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                UPDATE Balance
                SET balanceCode = %s, userID = %s, lastUpdate = CURRENT_TIMESTAMP
                WHERE idBalance = %s 
                """,(balance_code,user_id,balance_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un Error:{e}")
        return False
    finally:
        cursor.close()
        db.close()
    return True

def delete_balance(balance_id, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                    UPDATE Balance
                    SET status = 0, userID = %s, lastUpdate = CURRENT_TIMESTAMP
                    WHERE idBalance = %s
                    """,(user_id,balance_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()
    return True