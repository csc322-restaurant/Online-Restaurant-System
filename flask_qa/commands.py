import click
from flask.cli import with_appcontext

from .extensions import db
from .models import Restaurant, User,\
    Rating, Salary, Warnings, Question, \
    Ingredient, Supplier, Ingredientsupplier, \
    Supplyorder, Ingredientorder, Food, Recipe, \
    Menu, Dish, Order, Orderfood

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.drop_all()
    db.create_all()
    restaurant1 = Restaurant(
        restaurant_name = 'sushirestaurant',
        latitude = 123,
        longitude = 45
    )
    restaurant2 = Restaurant(
        restaurant_name = 'sushirestaurant2',
        latitude = 1234,
        longitude = 455
    )
    admin = User(
        name='admin', 
        unhashed_password='admin',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Manager',
        requestedRole='Manager',
        restaurant_id=1,
        admin=True,
    )
    user1 = User(
        name='manager of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Manager',
        requestedRole='Manager',
        restaurant_id=1,
        admin=False,
    )
    user2 = User(
        name='manager of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Manager',
        requestedRole='Manager',
        restaurant_id=2,
        admin=False,
    )
    user3 = User(
        name='salesmanager of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Salesmanager',
        requestedRole='Salesmanager',
        restaurant_id=1,
        admin=False,
    )
    user4 = User(
        name='salesmanager2 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Salesmanager',
        requestedRole='Salesmanager',
        restaurant_id=1,
        admin=False,
    )
    user5 = User(
        name='salesmanager of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Salesmanager',
        requestedRole='Salesmanager',
        restaurant_id=2,
        admin=False,
    )
    user6 = User(
        name='salesmanager2 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Salesmanager',
        requestedRole='Salesmanager',
        restaurant_id=2,
        admin=False,
    )
    user7 = User(
        name='cook1 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Chef',
        requestedRole='Chef',
        restaurant_id=1,
        admin=False,
    )
    user8 = User(
        name='cook2 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Chef',
        requestedRole='Chef',
        restaurant_id=1,
        admin=False,
    )
    user9 = User(
        name='cook1 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Chef',
        requestedRole='Chef',
        restaurant_id=2,
        admin=False,
    )
    user10 = User(
        name='cook2 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Chef',
        requestedRole='Chef',
        restaurant_id=2,
        admin=False,
    )
    user11 = User(
        name='deliverer1 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Deliverer',
        requestedRole='Deliverer',
        restaurant_id=1,
        admin=False,
    )
    user12 = User(
        name='deliverer2 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Deliverer',
        requestedRole='Deliverer',
        restaurant_id=1,
        admin=False,
    )
    user13 = User(
        name='deliverer1 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Deliverer',
        requestedRole='Deliverer',
        restaurant_id=2,
        admin=False,
    )
    user14 = User(
        name='deliverer2 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Deliverer',
        requestedRole='Deliverer',
        restaurant_id=2,
        admin=False,
    )
    user15 = User(
        name='registered1 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Registered',
        requestedRole='Registered',
        restaurant_id=1,
        admin=False,
    )
    user16 = User(
        name='registered2 of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Registered',
        requestedRole='Registered',
        restaurant_id=1,
        admin=False,
    )
    user17 = User(
        name='registered1 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Registered',
        requestedRole='Registered',
        restaurant_id=2,
        admin=False,
    )
    user18 = User(
        name='registered2 of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Registered',
        requestedRole='Registered',
        restaurant_id=2,
        admin=False,
    )
    user19 = User(
        name='visitor1 requesting registered of rest1', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Visitor',
        requestedRole='Registered',
        restaurant_id=1,
        admin=False,
    )
    user20 = User(
        name='visitor2 requesting registered of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Visitor',
        requestedRole='Registered',
        restaurant_id=2,
        admin=False,
    )
    user21 = User(
        name='visitor3 requesting chef of rest2', 
        unhashed_password='123',
        creditCardNumber=123,
        latitude=123,
        longitude=123,
        role='Visitor',
        requestedRole='Chef',
        restaurant_id=2,
        admin=False,
    )
    testRating = Rating(
        rating = 3,
        rated_id = 1,
        rater_id = 2
    )
    testSalary = Salary(
        user_id = 1,
        salary_value = 2
    )
    testWarnings = Warnings(
        user_id = 1,
        message = 'warning message'
    )
    testQuestion = Question(
        question = 'How is my question',
        answer = 'great answer',
        asked_by_id = 2,
        expert_id = 1
    )
    testIngredient = Ingredient(
        ingredient_name = 'vegetable'
    )
    testSupplier = Supplier(
        supplier_name = 'a company name for salary'
    )
    testIngredientsupplier = Ingredientsupplier(
        supplier_name = 'buying because vegatable',
        price = 4,
        ingredient_id = 1,
        supplier_id = 1
    )
    testSupplyorder = Supplyorder(
        supply_order_name = 'ordering for rest 1',
        approval = False,
        restaurant_id = 1
    )
    testIngredientorder = Ingredientorder(
        amount = 1,
        supply_order_id = 1,
        ingredient_supplier_id = 1
    )
    testFood = Food(
        food_name = 'sushi'
    )
    testRecipe = Recipe(
        food_id = 1,
        ingredient_supplier_id = 1
    )
    testMenu = Menu(
        menu_name = 'first menu'
    )
    testDish = Dish(
        price = 1,
        menu_id = 1,
        food_id = 1
    )
    testOrder = Order(
        order_success = False,
        user_id = 1,
        restaurant_id = 1
    )
    testOrderfood = Orderfood(
        dish_id = 1,
        order_id = 1
    )
    db.session.add(restaurant1)
    db.session.add(restaurant2)
    db.session.add(admin)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)
    db.session.add(user9)
    db.session.add(user10)
    db.session.add(user11)
    db.session.add(user12)
    db.session.add(user13)
    db.session.add(user14)
    db.session.add(user15)
    db.session.add(user16)
    db.session.add(user17)
    db.session.add(user18)
    db.session.add(user19)
    db.session.add(user20)
    db.session.add(user21)
    db.session.add(testRating)
    db.session.add(testSalary)
    db.session.add(testWarnings)
    db.session.add(testQuestion)
    db.session.add(testIngredient)
    db.session.add(testSupplier)
    db.session.add(testIngredientsupplier)
    db.session.add(testSupplyorder)
    db.session.add(testIngredientorder)
    db.session.add(testFood)
    db.session.add(testRecipe)
    db.session.add(testMenu)
    db.session.add(testDish)
    db.session.add(testOrder)
    db.session.add(testOrderfood)
    db.session.commit()
    