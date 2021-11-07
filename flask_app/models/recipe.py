from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
DATE_REGEX = re.compile(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')

class Recipe:
    db_name = "recipes_schema"
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.under30 = data["under30"]
        self.date_made = data["date_made"]
        self.user_id = data['user_id']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, under30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(under30)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_recipes = []
        for row in results:
            print(row['date_made'])
            all_recipes.append(cls(row))
        return all_recipes

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, under30 =%(under30)s, date_made=%(date_made)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
                flash("Recipe name must be at least 3 characters.", "recipe")
        if len(recipe['description']) < 3:
                flash("Recipe description be at least 3 characters.", "recipe")
                is_valid = False
        if len(recipe['instruction']) < 3:
                flash("Recipe instruction must be at least 3 characters long.", "recipe")
                is_valid = False
        if not DATE_REGEX.match(recipe['date_made']): 
                flash("Invalid date format!", "recipe")
                is_valid = False
        return is_valid
    
