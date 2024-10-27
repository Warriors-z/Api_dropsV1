from ..config import get_db_connection

def get_all_therapies():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT 
                    T.idTherapy AS idTherapy, 
                    P.ci AS ciNurse, 
                    PT.ci AS ciPatient, 
                    T.stretcherNumber AS stretcherNumber, 
                    IFNULL(T.startDate, 'No Iniciado') AS startDate, 
                    IFNULL(T.finishDate,'Sin fecha de Fin') AS finishDate 
                FROM 
                    Therapy T
                INNER JOIN 
                    Assignment A ON A.idTherapy = T.idTherapy
                INNER JOIN 
                    Nurse N ON N.idNurse = A.idNurse
                INNER JOIN 
                    Employee E ON E.idEmployee = N.idEmployee
                INNER JOIN 
                    Person P ON P.idPerson = E.idPerson
                INNER JOIN 
                    Person PT ON PT.idPerson = T.idPerson
                WHERE 
                    P.status = 1 
                    AND T.status = 1 
                    AND PT.status = 1
                ORDER BY 
                    T.idTherapy ASC
                

                """)
    therapies = cursor.fetchall()
    cursor.close()
    db.close()

    return therapies

def get_therapy_by_id(therapy_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT 
                    T.idTherapy AS idTherapy, 
                    P.ci AS ciNurse, 
                    PT.ci AS ciPatient, 
                    T.stretcherNumber AS stretcherNumber, 
                    IFNULL(T.startDate, 'No Iniciado') AS startDate, 
                    IFNULL(T.finishDate,'Sin fecha de Fin') AS finishDate 
                FROM 
                    Therapy T
                INNER JOIN 
                    Assignment A ON A.idTherapy = T.idTherapy
                INNER JOIN 
                    Nurse N ON N.idNurse = A.idNurse
                INNER JOIN 
                    Employee E ON E.idEmployee = N.idEmployee
                INNER JOIN 
                    Person P ON P.idPerson = E.idPerson
                INNER JOIN 
                    Person PT ON PT.idPerson = T.idPerson
                WHERE 
                    P.status = 1 
                    AND N.nurseOnTurn = 1 
                    AND T.status = 1 
                    AND PT.status = 1
                    AND T.idTherapy = %s
                """, (therapy_id,))
    therapy = cursor.fetchone()
    cursor.close()
    db.close()

    return therapy

def create_therapy(stretcher_number, id_balance, id_patient, id_nurse, user_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
                    INSERT INTO Therapy (stretcherNumber, idBalance, idPerson, userID)
                    VALUES (%s, %s, %s, %s)
                    """, (stretcher_number, id_balance, id_patient, user_id))
        
        id_therapy = cursor.lastrowid

        cursor.execute("""
                    INSERT INTO Assignment (idTherapy, idNurse)
                    VALUES (%s, %s)
                    """, (id_therapy, id_nurse))
        
        cursor.execute("""
                    UPDATE Nurse
                    SET nurseOnTurn = 0
                    WHERE idNurse = %s
                    """,(id_nurse,))
        cursor.execute("""
                    UPDATE Balance
                    SET available = 0
                    WHERE idBalance = %s
                    """,(id_balance,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()
    return True

def update_therapy(therapy_id):
    return True

def delete_therapy(therapy_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("UPDATE Therapy SET status = 0 WHERE idTherapy = %s",(therapy_id,))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Ocurrio un Error: {e}")
        return False
    finally:
        cursor.close()
        db.close()
    return True

def get_info_therapy(therapy_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                SELECT 
                    T.idTherapy AS idTherapy, 
                    P.ci AS ciNurse, 
                    PT.ci AS ciPatient, 
                    T.stretcherNumber AS stretcherNumber, 
                    IFNULL(T.startDate, 'No Iniciado') AS startDate, 
                    IFNULL(T.finishDate, 'Sin fecha de Fin') AS finishDate,
                    IFNULL(A.startDate, 'No Iniciado') AS startDateAssing,
                    IFNULL(A.finishDate, 'Sin fecha de Fin') AS finishDateAssing,
                    IFNULL(T.suggestedTime, 'Sin Información') AS idealTime, 
                    IFNULL(TIMESTAMPDIFF(HOUR, T.startDate, T.finishDate), 'Sin tiempo total') AS totalTime,
                    IFNULL(T.volume, 'Sin Volumen') AS volumen,
                    IFNULL(SUM(CASE WHEN S.alert = 1 THEN 1 ELSE 0 END), 0) AS numberBubbles,
                    IFNULL(SUM(CASE WHEN S.alert = 2 THEN 1 ELSE 0 END), 0) AS numberBlocks,
                    IFNULL(SUM(CASE WHEN S.alert = 3 THEN 1 ELSE 0 END), 0) AS numberBoth
                    FROM Therapy T
                    LEFT JOIN Assignment A ON A.idTherapy = T.idTherapy
                    LEFT JOIN Nurse N ON N.idNurse = A.idNurse
                    LEFT JOIN Employee E ON E.idEmployee = N.idEmployee
                    LEFT JOIN Person P ON P.idPerson = E.idPerson
                    LEFT JOIN Person PT ON PT.idPerson = T.idPerson
                    LEFT JOIN Sample S ON S.idTherapy = T.idTherapy
                    WHERE T.idTherapy = %s
                    AND P.status = 1
                    
                    AND PT.status = 1
                    AND T.status = 1
                    GROUP BY T.idTherapy, P.ci, PT.ci, T.stretcherNumber, T.startDate, T.finishDate,A.startDate,A.finishDate, T.suggestedTime, T.volume;
                """, (therapy_id,))
    therapy = cursor.fetchone()
    cursor.close()
    db.close()
    return therapy

def get_all_nurses():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                    SELECT N.idNurse, CONCAT(P.name,' ',P.lastName,' ', P.secondLastName) AS fullName, N.nurseRole AS role
                    FROM Nurse N
                    INNER JOIN Employee E ON E.idEmployee = N.idEmployee
                    INNER JOIN Person P ON P.idPerson = E.idPerson
                    WHERE P.status = 1 AND N.nurseOnTurn = 1
                """)
    nurses = cursor.fetchall()
    cursor.close()
    db.close()
    return nurses

def get_all_patients():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                    SELECT idPerson, CONCAT(name, ' ',lastName,' ', secondLastName) AS patient, ci
                    FROM Person
                    WHERE status = 1
                """)
    patients = cursor.fetchall()
    cursor.close()
    db.close()
    return patients

def get_all_balances():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
                    SELECT idBalance, balanceCode AS code
                    FROM Balance
                    WHERE status = 1 AND available = 1
                """)
    balances = cursor.fetchall()
    cursor.close()
    db.close()
    return balances