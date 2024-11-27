from ..config import get_db_connection

def get_all_therapies():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.callproc("GetActiveTherapies")
            therapies = []
            for result_set in cursor.stored_results():
                therapies = result_set.fetchall() 
                break 
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        therapies = None
    finally:
        db.close()
    return therapies


def create_therapy(therapy):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            print(therapy.stretcher_number)
            print(therapy.balance_id)
            print(therapy.nurse_id)
            print(therapy.user_id)
            print(therapy.patient_id)
            cursor.callproc("InsertTherapy", 
                (therapy.stretcher_number, therapy.balance_id, therapy.nurse_id, therapy.user_id, therapy.patient_id))
            result = None
            for result_set in cursor.stored_results():
                result = result_set.fetchone()
                print(result)
            db.commit()
        return result
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return None
    finally:
        db.close()

def get_info_therapy(therapy_id):
    therapy = None
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.callproc("""GetTherapyDetails""", (therapy_id,))
            for result in cursor.stored_results():
                therapy = result.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return therapy

def get_all_therapies_nurses(nurse_id):
    therapies = []
    try: 
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.callproc("""GetNurseTherapies""", (nurse_id,))
            for result in cursor.stored_results():
                therapies = result.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return therapies

def get_all_therapies_asign():
    therapies = []
    try: 
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.callproc("""GetAllNurseTherapies""")
            for result in cursor.stored_results():
                therapies = result.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally:
        db.close()
    return therapies

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