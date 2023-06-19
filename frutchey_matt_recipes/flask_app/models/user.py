from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

#! CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL('recipes').query_db(query, data)
        return result

#! READ ONE:
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return cls(result[0])
        return None

#! VALIDATION
    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;" 
        existing_email = connectToMySQL('recipes').query_db(query, user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 letters.", category = 'register')
            is_valid = False
        if not user['first_name'].isalpha():
            flash("Please enter only letters for your first name.", category = 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Please enter a valid email address.", category = 'register')
            is_valid = False
        if len(existing_email) >= 1:
            flash("Email is already registered. Please enter a different one.", category = 'register')
            is_valid = False
        if len(user['password']) < 6:
            flash("Password must be at least six characters.", category = 'register')
            is_valid = False
        if user['password'] != user['confirm_pw']:
            flash("Passwords do not match. Please try again.", category = 'register')
            is_valid = False
        return is_valid
