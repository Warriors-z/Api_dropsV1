from ..config import get_db_connection

def get_all_patients():
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT idPatient AS idPatient, name, lastName,IFNULL(secondLastName, 'No tiene') AS secondLastName, birthDate, genre, ci, registerDate, IFNULL(lastUpdate, 'Sin Cambios') AS lastUpdate
                FROM Patient
                WHERE status = 1;
                """)
            patients = cursor.fetchall()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
    finally: 
        db.close()

    return patients

def get_patient_by_id(patient_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT idPatient AS idPatient, name, lastName,IFNULL(secondLastName, 'No tiene') AS secondLastName, birthDate, genre, ci, registerDate, IFNULL(lastUpdate, 'Sin Cambios') AS lastUpdate
                FROM Patient
                WHERE status = 1 AND idPatient = %s;
                """,(patient_id,))
            patient = cursor.fetchone()
    except Exception as e:
        print(f"Ocurrio un error: {e}")
        patient = None
    finally:
        db.close()

    return patient


def check_exists_patient(ci):
    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT ci FROM Patient WHERE ci  = %s
            """, (ci,))
            result = cursor.fetchall()
            if result:
                ci = result[0]
                return ci
            else:
                return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None
    finally:
        db.close()

def create_patient(patient):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            print(patient.user_id)
            cursor.execute("""
                    INSERT INTO Patient(name,lastName,secondLastName,birthDate, genre, ci, userID)
                    VALUES (%s,%s,NULLIF(%s,''),%s,%s,%s,%s)
                    """,(patient.name,patient.last_name,patient.second_last_name,patient.birth_date, patient.genre,patient.ci,patient.user_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def update_patient(patient):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            print(f"El apellido es {patient.second_last_name}")
            cursor.execute("""
                    UPDATE Patient
                    SET name = %s, lastName = %s, secondLastName = NULLIF(%s,''), birthDate = %s, genre = %s ,ci = %s, userID = %s, lastUpdate = CURRENT_TIMESTAMP
                    WHERE idPatient = %s
                    """,(patient.name,patient.last_name, patient.second_last_name, patient.birth_date, patient.genre, patient.ci, patient.user_id, patient.patient_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()

def delete_patient(patient_id, user_id):
    try:
        db = get_db_connection()
        with db.cursor(dictionary=True) as cursor:
            cursor.execute("""
                    UPDATE Patient
                    SET status = 0, userID = %s, lastUpdate = CURRENT_TIMESTAMP
                    WHERE idPatient = %s AND status = 1
                    """,(user_id,patient_id,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Ocurrió un error: {e}")
        return False
    finally:
        db.close()
    