from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.datemade = data['datemade']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chef = None

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, datemade, time, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(datemade)s, %(time)s, NOW(), NOW(), %(user_id)s);"
        result = connectToMySQL('recipes').query_db(query, data)
        return result

#! Read
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
            #? Select all - from current table - join other table - on this table's f.key - where it is the same on the other table's primary key
        results = connectToMySQL('recipes').query_db(query)
        print(results) #! Works so far - Tested in Workbench
        all_recipes = []
        for result in results:
            one_recipe = cls(result)
            user_info = {
                "id": result['users.id'], # Specified because of two 'id's
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": result['password'],
                "created_at": result["users.created_at"], # Same as above
                "updated_at": result["users.updated_at"] # Same as above
            }
            one_recipe.chef = User(user_info)
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users on recipes.user_id = users.id WHERE recipes.id = %(id)s" # Works in WB
        results = connectToMySQL('recipes').query_db(query, data)
        if results:
            result = results[0]
            this_recipe = cls(result)
            user_info = {
                    "id": result['users.id'], # Specified because of two 'id's
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "email": result['email'],
                    "password": result['password'],
                    "created_at": result["users.created_at"], # Same as above
                    "updated_at": result["users.updated_at"] # Same as above
            }
            this_recipe.chef = User(user_info)
            return this_recipe
        else:
            return None

#! Update
    @classmethod
    def edit_one_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, datemade = %(datemade)s, time = %(time)s WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

#! Delete
    @classmethod
    def delete_recipe(cls, recipe_id):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        data = {
            "recipe_id": recipe_id
        }
        return connectToMySQL('recipes').query_db(query, data)

#! Validate
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Please provide a name of at least 3 letters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Please enter a description of at least 3 letters. 'Tasty', perhaps?")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Please provide at least 3 letters about how to make this.")
            is_valid = False
        if not (recipe['datemade']):
            flash("Please tell us when you last made this dish.")
            is_valid = False
        if 'time' not in recipe:
            flash("Please tell us if this recipes takes over or under 30 minutes.")
            is_valid = False
        return is_valid