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
        restaurant_name = 'Tamashi Sushi',
        latitude = 123,
        longitude = 45
    )
    restaurant2 = Restaurant(
        restaurant_name = 'Ariyoshi',
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
   
    ingredient1 = Ingredient(
        ingredient_name = 'Seaweed'
    )
    ingredient2 = Ingredient(
        ingredient_name = 'Shrimp'
    )
    ingredient3 = Ingredient(
        ingredient_name = 'Tuna'
    )
    ingredient4 = Ingredient(
        ingredient_name = 'Salmon'
    )
    ingredient5 = Ingredient(
        ingredient_name = 'Rice'
    )
    ingredient6 = Ingredient(
        ingredient_name = 'Cucumber'
    )
    ingredient7 = Ingredient(
        ingredient_name = 'Sushi Vinegar'
    )
    supplier1 = Supplier(
        supplier_name = 'Fresh Seafood'
    )
    supplier2 = Supplier(
        supplier_name = 'Umi'
    )
    supplier3 = Supplier(
        supplier_name = 'Blue Ocean'
    )
    ingredientSupplier1 = Ingredientsupplier(
        supplier_name = 'Fresh Seafood',
        price = 2.20,
        ingredient_id = 1,
        supplier_id = 1
    )
    ingredientSupplier2 = Ingredientsupplier(
        supplier_name = 'Fresh Seafood',
        price = 3.10,
        ingredient_id = 3,
        supplier_id = 1
    )
    ingredientSupplier3 = Ingredientsupplier(
        supplier_name = 'Umi',
        price = 2.75,
        ingredient_id = 5,
        supplier_id = 2
    )
    ingredientSupplier4 = Ingredientsupplier(
        supplier_name = 'Umi',
        price = 4.33,
        ingredient_id = 2,
        supplier_id = 2
    )
    ingredientSupplier5 = Ingredientsupplier(
        supplier_name = 'Blue Ocean',
        price = 3.87,
        ingredient_id = 4,
        supplier_id = 3
    )
    ingredientSupplier6 = Ingredientsupplier(
        supplier_name = 'Blue Ocean',
        price = 1.22,
        ingredient_id = 6,
        supplier_id = 3
    )
    ingredientSupplier7 = Ingredientsupplier(
        supplier_name = 'Umi',
        price = 2.25,
        ingredient_id = 7,
        supplier_id = 2
    )
    supplyOrder1 = Supplyorder(
        supply_order_name = 'Order for Tamashi Sushi',
        approval = False,
        restaurant_id = 1
    )
    supplyOrder2 = Supplyorder(
        supply_order_name = 'Order for Ariyoshi',
        approval = False,
        restaurant_id = 2
    )
    ingredientOrder1 = Ingredientorder(
        amount = 20,
        supply_order_id = 1,
        ingredient_supplier_id = 3
    )
    ingredientOrder2 = Ingredientorder(
        amount = 15,
        supply_order_id = 1,
        ingredient_supplier_id = 5
    )
    ingredientOrder3 = Ingredientorder(
        amount = 8,
        supply_order_id = 2,
        ingredient_supplier_id = 4
    )
    food1 = Food(
        food_name = 'Shrimp Sushi'
    )
    food2 = Food(
        food_name = 'Salmon Sushi'
    )
    food3 = Food(
        food_name = 'Cucumber Roll'
    )
    recipe1 = Recipe(
        food_id = 1,
        ingredient_supplier_id = 1
    )
    recipe2 = Recipe(
        food_id = 1,
        ingredient_supplier_id = 2
    )
    recipe3 = Recipe(
        food_id = 1,
        ingredient_supplier_id = 2
    )
    recipe4 = Recipe(
        food_id = 2,
        ingredient_supplier_id = 3
    )
    recipe5 = Recipe(
        food_id = 2,
        ingredient_supplier_id = 2
    )
    recipe6 = Recipe(
        food_id = 2,
        ingredient_supplier_id = 2
    )
    recipe7 = Recipe(
        food_id = 3,
        ingredient_supplier_id = 1
    )
    recipe8 = Recipe(
        food_id = 3,
        ingredient_supplier_id = 2
    )
    recipe9 = Recipe(
        food_id = 3,
        ingredient_supplier_id = 3
    )
    menu1 = Menu(
        menu_name = 'Tamashi Sushi Menu',
        restaurant_id = 1
    )
    menu2 = Menu(
        menu_name = 'Ariyoshi Menu',
        restaurant_id = 2
    )
    dish1 = Dish(
        price = 3.50,
        menu_id = 1,
        food_id = 1
    )
    dish2 = Dish(
        price = 4.20,
        menu_id = 2,
        food_id = 2
    )
    order1 = Order(
        order_success = False,
        user_id = 15,
        restaurant_id = 1
    )
    order2 = Order(
        order_success = False,
        user_id = 17,
        restaurant_id = 2
    )
    orderFood1 = Orderfood(
        dish_id = 1,
        order_id = 1
    )
    orderFood2 = Orderfood(
        dish_id = 2,
        order_id = 1
    )
    orderFood3 = Orderfood(
        dish_id = 2,
        order_id = 2
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
    db.session.add(ingredient1)
    db.session.add(ingredient2)
    db.session.add(ingredient3)
    db.session.add(ingredient4)
    db.session.add(ingredient5)
    db.session.add(ingredient6)
    db.session.add(ingredient7)
    db.session.add(supplier1)
    db.session.add(supplier2)
    db.session.add(supplier3)
    db.session.add(ingredientSupplier1)
    db.session.add(ingredientSupplier2)
    db.session.add(ingredientSupplier3)
    db.session.add(ingredientSupplier4)
    db.session.add(ingredientSupplier5)
    db.session.add(ingredientSupplier6)
    db.session.add(ingredientSupplier7)
    db.session.add(supplyOrder1)
    db.session.add(supplyOrder2)
    db.session.add(ingredientOrder1)
    db.session.add(ingredientOrder2)
    db.session.add(ingredientOrder3)
    db.session.add(food1)
    db.session.add(food2)
    db.session.add(food3)
    db.session.add(recipe1)
    db.session.add(recipe2)
    db.session.add(recipe3)
    db.session.add(recipe4)
    db.session.add(recipe5)
    db.session.add(recipe6)
    db.session.add(recipe7)
    db.session.add(recipe8)
    db.session.add(recipe9)
    db.session.add(menu1)
    db.session.add(menu2)
    db.session.add(dish1)
    db.session.add(dish2)
    db.session.add(order1)
    db.session.add(order2)
    db.session.add(orderFood1)
    db.session.add(orderFood2)
    db.session.add(orderFood3)
    db.session.commit()
    