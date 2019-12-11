from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import DateTime
import datetime
from .extensions import db 

#restaurant, we will have to make some ourselves as admin to place these in
class Restaurant(db.Model):
    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name =  db.Column(db.String(50))
    latitude = db.Column(db.Float(8))
    longitude = db.Column(db.Float(8))

    #ingredient order restaurant
    user_of_restaurant = db.relationship(
        'User', 
        foreign_keys='User.restaurant_id', 
        backref='user_of_restaurant', 
        lazy=True
    )

    menu_of_restaurant = db.relationship(
        'Menu', 
        foreign_keys='Menu.restaurant_id', 
        backref='menu_of_restaurant', 
        lazy=True
    )

    #ingredient order restaurant
    restaurant_orders = db.relationship(
        'Supplyorder', 
        foreign_keys='Supplyorder.restaurant_id', 
        backref='order_from_restaurant', 
        lazy=True
    )

    #customer order restaurant
    restaurant_has_orders = db.relationship(
        'Order', 
        foreign_keys='Order.restaurant_id', 
        backref='customer_ordered', 
        lazy=True
    )

#user can be a visitor, registered, delivery, chef, salesperson, or manager
#to make an admin we have to enable it, for now ill place an entry on registration
#to allow to be an admin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    creditCardNumber = db.Column(db.Integer, nullable=False, default=123)
    latitude = db.Column(db.Float(8), nullable=False, default=123)
    longitude = db.Column(db.Float(8), nullable=False, default=123)
    role = db.Column(db.String(50))
    requestedRole = db.Column(db.String(50), nullable=False, default='visitor')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))
    admin = db.Column(db.Boolean)

    questions_asked = db.relationship(
        'Question', 
        foreign_keys='Question.asked_by_id', 
        backref='asker', 
        lazy=True
    )

    answers_requested = db.relationship(
        'Question',
        foreign_keys='Question.expert_id',
        backref='expert',
        lazy=True
    )

    #gets the rater
    users_rated = db.relationship(
        'Rating', 
        foreign_keys='Rating.rater_id', 
        backref='rater', 
        lazy=True
    )

    #gets the rated
    ratings_user_received = db.relationship(
        'Rating',
        foreign_keys='Rating.rated_id',
        backref='rated',
        lazy=True
    )

    #gets the salary
    salary_user_has = db.relationship(
        'Salary',
        foreign_keys='Salary.user_id',
        backref='payreciever',
        lazy=True
    )

    #gets the warnings of the user
    user_warning = db.relationship(
        'Warnings',
        foreign_keys='Warnings.user_id',
        backref='userwarned',
        lazy=True
    )
    #gets the orders of the user
    user_orders = db.relationship(
        'Order',
        foreign_keys='Order.user_id',
        backref='order_to',
        lazy=True
    )
    #gets the orders of the user
    delivery_orders = db.relationship(
        'Order',
        foreign_keys='Order.deliverer_id',
        backref='order_from_user',
        lazy=True
    )
    #gets the orders of the user
    cookof = db.relationship(
        'Dish',
        foreign_keys='Dish.user_id',
        backref='iscook',
        lazy=True
    )
    #gets the ratings of the user on food
    food_rating = db.relationship(
        'Dishrating',
        foreign_keys='Dishrating.user_id',
        backref='food_rating',
        lazy=True
    )

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

#rating list from and to a user
class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=3)
    message = db.Column(db.String(50), default='rating desc')
    rating_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    rated_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#salary of each user - registered and visitors should not be have a salary
class Salary(db.Model):
    salary_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    salary_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    salary_value = db.Column(db.Float, nullable=False, default=0)

#user will get warnned when recent ratings are below standard
class Warnings(db.Model):
    warning_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    warning_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.String(50), nullable=False, default='warning')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    question_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    asked_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expert_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#list of ingredients
class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name =  db.Column(db.String(50), nullable=False, default='default ingredient')

    #ingredient by supplier
    ingredient_supplies = db.relationship(
        'Ingredientsupplier', 
        foreign_keys='Ingredientsupplier.ingredient_id', 
        backref='supply_ingredient', 
        lazy=True
    )
    
#list of suppliers
class Supplier(db.Model):
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name =  db.Column(db.String(50), nullable=False, default='supplier')

    #ingredient by supplier
    supplier_offer = db.relationship(
        'Ingredientsupplier', 
        foreign_keys='Ingredientsupplier.supplier_id', 
        backref='ingredient_supplier', 
        lazy=True
    )

#list of suppliers and ingredients with their price of it
class Ingredientsupplier(db.Model):
    ingredient_supplier_id = db.Column(db.Integer, primary_key=True)
    update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    price = db.Column(db.Float, nullable=False, default=1)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'))

    #ingredient by supplier
    order_from_supplier = db.relationship(
        'Ingredientorder', 
        foreign_keys='Ingredientorder.ingredient_supplier_id', 
        backref='ingredient_order', 
        lazy=True
    )
    #ingredients in each food_item
    ingredients_in_dish = db.relationship(
        'Recipe', 
        foreign_keys='Recipe.ingredient_supplier_id', 
        backref='recipe_ingredient', 
        lazy=True
    )

#tables is what salesman make
class Supplyorder(db.Model):
    supply_order_id = db.Column(db.Integer, primary_key=True)
    supply_order_name = db.Column(db.String(50), nullable=False, default='restaurant supply order')
    approval = db.Column(db.Boolean, default=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))

    #each of the ingredient order
    order_ingredients = db.relationship(
        'Ingredientorder', 
        foreign_keys='Ingredientorder.supply_order_id', 
        backref='supply_order', 
        lazy=True
    )

#for each supply order this table shows the order of each ingredient
class Ingredientorder(db.Model):
    ingredient_order_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False, default=1)
    added_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    supply_order_id = db.Column(db.Integer, db.ForeignKey('supplyorder.supply_order_id'))
    ingredient_supplier_id = db.Column(db.Integer, db.ForeignKey('ingredientsupplier.ingredient_supplier_id'))
    
#fooditems made by chefs
class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    food_name =  db.Column(db.String(50), nullable=False, default='food')
    #the food item can be in a menu
    food_in_menu = db.relationship(
        'Dish', 
        foreign_keys='Dish.food_id', 
        backref='menu_has_Food', 
        lazy=True
    )

#what ingredients are in each food item
class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'))
    ingredient_supplier_id = db.Column(db.Integer, db.ForeignKey('ingredientsupplier.ingredient_supplier_id'))

#any chef can make a menu
class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True)
    menu_name =  db.Column(db.String(50), nullable=False, default='menu')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))
    #each menu has ingredients
    menu_has_fooditems = db.relationship(
        'Dish', 
        foreign_keys='Dish.menu_id', 
        backref='is_in_menu', 
        lazy=True
    )

#Any chef can add fooditems to a menu
class Dish(db.Model):
    dish_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False, default=0.00)
    dish_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.food_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #each dish can have orders
    dish_in_orders = db.relationship(
        'Orderfood', 
        foreign_keys='Orderfood.dish_id', 
        backref='orders_has_dish', 
        lazy=True
    )
    #each dish can have ratings
    ratings_of_dish = db.relationship(
        'Dishrating', 
        foreign_keys='Dishrating.dish_id', 
        backref='dish_in_ratings', 
        lazy=True
    )
#Any chef can add fooditems to a menu
class Dishrating(db.Model):
    Dishrating_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#any chef can make a menu
class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_success = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    deliverer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id= db.Column(db.Integer, db.ForeignKey('restaurant.restaurant_id'))
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    #each dish can have orders
    orders_has_food = db.relationship(
        'Orderfood', 
        foreign_keys='Orderfood.order_id', 
        backref='food_in_orders', 
        lazy=True
    )

#any chef can make a menu
class Orderfood(db.Model):
    orderfood_id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))



