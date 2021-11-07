from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = "recipes_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password  = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        #list to add recipes associated with user
        self.recipes = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users 

    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) <1:
            return False 
        return cls(results[0])

    @classmethod
    def get_from_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) <1:
            return False 
        return cls(results[0])  
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
        
    @classmethod
    def get_user_with_recipes(cls,data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(f"results of join query get recipes {results[0]}")
        user = cls(results[0])

        for row_from_db in results:
            recipe_data = {
                "id":row_from_db["recipes.id"],
                "name": row_from_db["name"],
                "description": row_from_db['description'],
                "instruction":row_from_db['instruction'],
                "under30":row_from_db["under30"],
                "date_made":row_from_db["date_made"],
                "user_id":row_from_db["user_id"],
                "created_at": row_from_db["recipes.created_at"],
                "updated_at": row_from_db["recipes.updated_at"]
            }
            user.recipes.append(recipe.Recipe(recipe_data))
        
        return user #return user with list of recipe objects 

    @staticmethod
    def validate(form):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db_name).query_db(query,form)
        if result:
            if len(result) >=1: #email already in database
                    flash("Email already taken.","register")
                    is_valid=False
            # test whether a field matches the pattern
        if not EMAIL_REGEX.match(form['email']): 
                flash("Invalid email address!", "register")
                is_valid = False
        if len(form['first_name']) < 2:
                flash("First name must be at least 2 characters.", "register")
        if len(form['last_name']) < 2:
                flash("Last name must be at least 2 characters.", "register")
                is_valid = False
        if len(form['password']) < 6:
                flash("Password must be at least 6 characters long.", "register")
                is_valid = False
        if form['password'] != form['confirm']:
                flash("Your password don't match!", "register")
                is_valid = False
        return is_valid




