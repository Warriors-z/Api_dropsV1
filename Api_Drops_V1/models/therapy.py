from ..config import get_db_connection

def get_all_therapies():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetActiveTherapies(); """)
            therapies = cursor.fetchall() 
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()

    return therapies

def create_therapy(therapy):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL InsertTherapy(%s,%s,%s,%s,%s);""", 
                (therapy.stretcher_number, therapy.balance_id, therapy.nurse_id, therapy.user_id, therapy.patient_id))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def get_info_therapy(therapy_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetTherapyDetails(%s); """, (therapy_id,))
            therapy = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return therapy

def get_all_nurses():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute(""" CALL GetActiveNurses(); """)
            nurses = cursor.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return nurses

def get_all_patients():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                    SELECT idPatient, CONCAT(name, ' ',lastName,' ', secondLastName) AS patient, ci
                    FROM Patient
                    WHERE status = 1
                """)
            patients = cursor.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return patients

def get_all_balances():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                    SELECT idBalance, balanceCode AS code
                    FROM Balance
                    WHERE status = 1 AND available = 1
                """)
            balances = cursor.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return balances