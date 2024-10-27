from ..config import get_db_connection

def get_all_patients():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT idPerson AS idPatient, name, lastName,IFNULL(secondLastName, 'No tiene') AS secondLastName, birthDate, ci, registerDate, IFNULL(lastUpdate, 'Sin Cambios') AS lastUpdate
                FROM Person
                WHERE status = 1;
                """)
    patients = cursor.fetchall()
    cursor.close()
    db.close()
    return patients

def get_patient_by_id(patient_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT idPerson AS idPatient, name, lastName,IFNULL(secondLastName, 'No tiene') AS secondLastName, birthDate, ci
                FROM Person
                WHERE status = 1 AND idPerson = %s;
                """,(patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    db.close()
    return patient

def create_patient(name, last_name, second_last_name, birth_date, ci, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                    INSERT INTO Person(name,lastName,secondLastName,birthDate, ci, userID)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    """,(name,last_name,second_last_name,birth_date,ci,user_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un error: {e}")
        return False
    finally:
        cursor.close()
        db.close
    return True

def update_patient(patient_id, name, last_name, second_last_name, birth_date, ci, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                    UPDATE Person
                    SET name = %s, lastName = %s, secondLastName = %s, birthDate = %s, ci = %s, userID = %s
                    WHERE idPerson = %s
                    """,(name,last_name, second_last_name, birth_date, ci, user_id, patient_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un error: {e}")
        return False
    finally:
        cursor.close()
        db.close
    return True

def delete_patient(patient_id, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                    UPDATE Person
                    SET status = 0, userID = %s
                    WHERE idPerson = %s
                    """,(user_id,patient_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()
    return True