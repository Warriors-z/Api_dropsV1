class Patient:
    def __init__(self, name, last_name,  birth_date, genre,ci, user_id,second_last_name=None, patient_id=None):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.genre = genre
        self.ci = ci
        self.user_id = user_id
        self.second_last_name = second_last_name
        self.patient_id = patient_id