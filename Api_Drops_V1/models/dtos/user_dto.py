class User:
    def __init__(self, name, last_name, email, address, birth_date, genre, ci,second_last_name=None,role_id=None,phone=None,user_id=None,user_name=None, password=None):
        self.user_name = user_name
        self.password = password 
        self.name = name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.birth_date = birth_date
        self.genre = genre
        self.ci = ci
        self.second_last_name = second_last_name
        self.role_id = role_id
        self.phone = phone      
        self.user_id = user_id