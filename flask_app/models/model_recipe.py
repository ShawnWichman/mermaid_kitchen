from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from datetime import datetime
import math


class Recipe:
    db = "chef_recipes"
    def __init__(self,data):
        self.id = data['id']
        self.user_id =data['user_id']
        self.name= data['name']
        self.description= data['description']
        self.instructions= data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #validate recipe model
    @staticmethod
    def is_valid(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid

    # get all recipes
    @classmethod
    def get_all(cls):
        query = 'SELECT * from recipes;'
        results = connectToMySQL(cls.db).query_db(query)
        recipes =[]
        for row in results:
            recipes.append(cls(row))
        return recipes

    # get one recipe
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    # edit a recipe
    @classmethod
    def update_one(cls, data):
        query = "UPDATE recipes SET user_id  = %(user_id)s, name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, date_made=%(date_made)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results


    #create a recipe
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, instructions, under30, date_made) VALUES ( %(user_id)s,%(name)s,%(description)s,%(instructions)s,%(under30)s,%(date_made)s)"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    #delete recipe
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id =%(id)s;"
        results =  connectToMySQL(cls.db).query_db(query,data)
        return results



