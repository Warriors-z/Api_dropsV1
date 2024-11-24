from ..config import get_db_connection

def create_maintenance(maintenance):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                    CALL InsertMaintenance(%s,%s,%s);
                    """, (maintenance.balance_id, maintenance.user_id, maintenance.last_factor,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un error: {e}")
        return False
    finally:
        db.close()

def get_balance_to_maintenance_by_code(balance_code):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" 
                    CALL GetBalanceToMaintenance(%s);W
                    );
                     """, (balance_code,))
            maintenance = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        maintenance = None
    finally:
        db.close()
    return maintenance

