from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import app
from .model_recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from .model_recipe import Recipe

class User:
    db = "chef_recipes"
    def __init__(self,data):
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes =[]

    #validate user model
    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data['first_name']) <2:
            flash("First name must be longer than two letters.")
            is_valid=False
        if len(data['last_name']) <2:
            flash("Last name must be longer than two letters.")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email")
            is_valid=False
        if User.get_by_email({'email': data['email']}):
            flash("Email taken.")
            is_valid=False
        if len(data['password']) <8:
            flash("Password must be at least 8 characters.")
            is_valid=False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match.")
            is_valid=False
        return is_valid

    # get user by email for login validation
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = connectToMySQL(cls.db).query_db(query,data)
        if data == ():
            return False
        else:
            return cls(data[0])

    # get user by id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    # register new user
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    #get all users
    @classmethod
    def get_all(cls):
        query = 'SELECT * from users'
        results = connectToMySQL(cls.db).query_db(query)
        users =[]
        for row in results:
            users.append(cls(row))
        return users

    #show user with their recipes
    @classmethod
    def get_user_with_recipes( cls , data ):
        query = "SELECT * FROM users LEFT JOIN recipes ON user_id = recipes.user_id WHERE user_id =%(id)s;"
        results = connectToMySQL(cls.db).query_db( query,data )
        print(results)
        user = cls(results[0])
        for row in results:
            recipe_data = {
                'id': row['recipes.id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'under30': row['under30'],
                'date_made': row['date_made'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id']
        }
            user.recipes.append(Recipe(recipe_data))
        return user





