from ..config import get_db_connection

def get_all_balances():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL  GetActiveBalances(); """)
            balances = cursor.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        balances = []
    finally: 
        db.close()

    return balances

def get_balance_by_id(balance_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetBalanceById(%s); """, (balance_id,))
            balance = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        balance = None
    finally:
        db.close()

    return balance

def check_exists_balance(balance_code):
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT balanceCode FROM Balance WHERE balanceCode  = %s
            """, (balance_code,))
            result = cursor.fetchall()
            if result:
                code_balance = result[0]
                return code_balance
            else:
                return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        db.close()

def create_balance(balance):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                CALL InsertBalance(%s,%s);
                """,(balance.balance_code,balance.user_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def update_balance(balance):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                UPDATE Balance
                SET balanceCode = %s, userID = %s, lastUpdate = CURRENT_TIMESTAMP
                WHERE idBalance = %s 
                """,(balance.balance_code, balance.user_id, balance.balance_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def delete_balance(balance):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            print(balance.user_id, balance.balance_id)
            cursor.execute("""
                    UPDATE Balance
                    SET status = 0, userID = %s, lastUpdate = CURRENT_TIMESTAMP
                    WHERE idBalance = %s AND status = 1
                    """,(balance.user_id, balance.balance_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()