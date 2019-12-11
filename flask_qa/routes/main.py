from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import func

from flask_qa.extensions import db

from flask_qa.models import Restaurant, User,\
    Rating, Salary, Warnings, Question, \
    Ingredient, Supplier, Ingredientsupplier, \
    Supplyorder, Ingredientorder, Food, Recipe, \
    Menu, Dish, Order, Orderfood
import logging
main = Blueprint('main', __name__)

@main.route('/')
def index():
    questions = Question.query.filter(Question.answer != None).all()

    context = {
        'questions' : questions
    }

    return render_template('home.html', **context)

@main.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        question = request.form['question']
        expert = request.form['expert']

        question = Question(
            question=question, 
            expert_id=expert, 
            asked_by_id=current_user.id
        )

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('main.index'))

    experts = User.query.filter(User.role != 'visitor').all()

    context = {
        'experts' : experts
    }

    return render_template('ask.html', **context)

@main.route('/answer/<int:question_id>', methods=['GET', 'POST'])
@login_required
def answer(question_id):
    if (current_user.role == 'Visitor'):
        return redirect(url_for('main.index'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.answer = request.form['answer']
        db.session.commit()

        return redirect(url_for('main.unanswered'))

    context = {
        'question' : question
    }

    return render_template('answer.html', **context)

@main.route('/question/<int:question_id>')
def question(question_id):
    question = Question.query.get_or_404(question_id)

    context = {
        'question' : question
    }

    return render_template('question.html', **context)

@main.route('/unanswered')
@login_required
def unanswered():
    if (current_user.role == 'Visitor'):
        return redirect(url_for('main.index'))

    unanswered_questions = Question.query\
        .filter_by(expert_id=current_user.id)\
        .filter(Question.answer == None)\
        .all()

    context = {
        'unanswered_questions' : unanswered_questions
    }

    return render_template('unanswered.html', **context)
    
@main.route('/salary/<int:salary_id>', methods=['GET', 'POST'])
@login_required
def salary(salary_id):
    if (current_user.role == 'Registered' or current_user.role == 'Visitor'):
        return redirect(url_for('main.index'))

    salary = Salary.query.get(int(salary_id))
    
    salary.salary_value = int(request.form['amount'])
    db.session.commit()

    return redirect(url_for('main.employee'))

@main.route('/employee')
@login_required
def employee():
    if not (current_user.role == 'Manager'):
        return redirect(url_for('main.index'))

    employees = db.session.query(User, Salary)\
        .filter(User.id == Salary.user_id)\
        .filter_by(restaurant_id = current_user.restaurant_id)\
        .filter(User.role != 'Registered')\
        .filter(User.role != 'Visitor')\
        .all()

    context = {
        'employees' : employees
    }

    return render_template('employee.html', **context)

@main.route('/salesorder')
@login_required
def salesorder():
    if not (current_user.role == 'Manager'):
        return redirect(url_for('main.index'))

    salesorder = db.session.query(Supplyorder)\
        .filter_by(restaurant_id = current_user.restaurant_id)\
        .all()

    context = {
        'salesorder' : salesorder
    }

    return render_template('salesorder.html', **context)

@main.route('/createsalesorder', methods=['GET', 'POST'])
@login_required
def createsalesorder():
    if (current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    order_description = request.form['salesordertext']
    salesorder = Supplyorder(
        supply_order_name = order_description,
        approval = False,
        restaurant_id = current_user.restaurant_id
    )
    db.session.add(salesorder)
    db.session.commit()

    return redirect(url_for('main.salesorder'))

@main.route('/accept/<int:supply_order_id>')
@login_required
def acceptorder(supply_order_id):
    if (current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    supplyorder = Supplyorder.query.get_or_404(supply_order_id)

    supplyorder.approval = True
    db.session.commit()

    return redirect(url_for('main.salesorder'))

@main.route('/addsalesingredient', methods=['GET', 'POST'])
@login_required
def addsalesingredient():
    if (current_user.role != 'Salesmanager' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    ingredientorder = Ingredientorder(
        supply_order_id = request.form['supply_order_id'],
        ingredient_supplier_id = request.form['ingredient_supplier_id'],
        amount = request.form['amount']
    )
    db.session.add(ingredientorder)
    db.session.commit()

    return redirect(url_for('main.managesalesorder'))

@main.route('/managesalesorder')
@login_required
def managesalesorder():
    if (current_user.role != 'Salesmanager' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    salesorderlist = db.session.query(Supplyorder,\
         Ingredientorder,Ingredientsupplier, Supplier, Ingredient)\
        .filter(Supplyorder.approval == False)\
        .filter(Supplyorder.supply_order_id == Ingredientorder.supply_order_id)\
        .filter(Supplyorder.restaurant_id == current_user.restaurant_id)\
        .filter(Ingredientorder.ingredient_supplier_id == Ingredientsupplier.ingredient_supplier_id)\
        .filter(Ingredientsupplier.ingredient_id == Ingredient.ingredient_id)\
        .filter(Ingredientsupplier.supplier_id == Supplier.supplier_id)\
        .order_by(Supplyorder.supply_order_id)\
        .all()
    ingredientsupplierlist = db.session.query(Ingredientsupplier, Supplier, Ingredient)\
        .filter(Ingredientsupplier.ingredient_id == Ingredient.ingredient_id)\
        .filter(Ingredientsupplier.supplier_id == Supplier.supplier_id)\
        .all()
    context = {
        'incompletesalesorder' : salesorderlist,
        'ingredientsupply' : ingredientsupplierlist
    }

    return render_template('managesalesorder.html', **context)

@main.route('/users')
@login_required
def users():
    if (current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    users = User.query.filter_by(restaurant_id = current_user.restaurant_id).all()

    context = {
        'users' : users
    }

    return render_template('users.html', **context)

@main.route('/promote/<int:user_id>')
@login_required
def promote(user_id):
    if (current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    user.role = user.requestedRole
    salary = Salary(
        user_id = user_id,
        salary_value = 0
    )
    db.session.add(salary)
    db.session.commit()

    return redirect(url_for('main.users'))

@main.route('/addingredient', methods=['GET', 'POST'])
@login_required
def addingredient():
    if (current_user.role != 'Salesmanager' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    ingredient = Ingredient(
        ingredient_name = request.form['ingredient_name']
    )
    db.session.add(ingredient)
    db.session.commit()

    return redirect(url_for('main.manageingredients'))

@main.route('/addsupplier', methods=['GET', 'POST'])
@login_required
def addsupplier():
    if (current_user.role != 'Salesmanager' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    supplier = Supplier(
        supplier_name = request.form['supplier_name']
    )
    db.session.add(supplier)
    db.session.commit()

    return redirect(url_for('main.manageingredients'))

@main.route('/addingredientsupplier', methods=['GET', 'POST'])
@login_required
def addingredientsupplier():
    if (current_user.role != 'Salesmanager' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    ingredientsupplier = Ingredientsupplier(
        price = request.form['price'],
        ingredient_id = request.form['ingredient_id'],
        supplier_id = request.form['supplier_id']
    )
    db.session.add(ingredientsupplier)
    db.session.commit()

    return redirect(url_for('main.manageingredients'))

@main.route('/manageingredients')
@login_required
def manageingredients():
    if (current_user.role != 'Salesmanager' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    suppliers = db.session.query(Supplier).all()
    ingredients = db.session.query(Ingredient).all()
    ingredientsuppliers = db.session.query(Ingredientsupplier, Supplier, Ingredient)\
        .filter(Ingredientsupplier.ingredient_id == Ingredient.ingredient_id)\
        .filter(Ingredientsupplier.supplier_id == Supplier.supplier_id)\
        .all()
    
    context = {
        'suppliers' : suppliers,
        'ingredients' : ingredients,
        'ingredientsuppliers' : ingredientsuppliers
    }

    return render_template('manageingredients.html', **context)

@main.route('/addmenu', methods=['GET', 'POST'])
@login_required
def addmenu():
    if (current_user.role != 'Chef' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    menu = Menu(
        menu_name = request.form['menu_name'],
        restaurant_id = current_user.restaurant_id
    )
    db.session.add(menu)
    db.session.commit()

    return redirect(url_for('main.managemenu'))

@main.route('/addfood', methods=['GET', 'POST'])
@login_required
def addfood():
    if (current_user.role != 'Chef' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    food = Food(
        food_name = request.form['food_name']
    )
    db.session.add(food)
    db.session.commit()

    return redirect(url_for('main.managemenu'))

@main.route('/addfoodtomenu', methods=['GET', 'POST'])
@login_required
def addfoodtomenu():
    if (current_user.role != 'Chef' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))

    dish = Dish(
        price = request.form['price'],
        menu_id = request.form['menu_id'],
        food_id = request.form['food_id']
    )
    db.session.add(dish)
    db.session.commit()

    return redirect(url_for('main.managemenu'))

@main.route('/deletefoodfrommenu', methods=['GET', 'POST'])
@login_required
def deletefoodfrommenu():
    if (current_user.role != 'Chef' and current_user.role != 'Manager'):
        return redirect(url_for('main.index'))
    Dish.query.filter_by(dish_id = request.form['dish_id']).delete()
    db.session.commit()

    return redirect(url_for('main.managemenu'))

@main.route('/managemenu')
@login_required
def managemenu():
    if (current_user.role != 'Manager' and current_user.role != 'Chef' ):
        return redirect(url_for('main.index'))

    menulist = db.session.query(Menu)\
        .filter_by(restaurant_id = current_user.restaurant_id)\
        .all()
    food = db.session.query(Food).all()
    menu = db.session.query(Menu, Dish, Food)\
        .filter(Menu.menu_id == Dish.dish_id)\
        .filter(Dish.food_id == Food.food_id)\
        .filter(Menu.restaurant_id == current_user.restaurant_id)\
        .order_by(Menu.menu_id)\
        .all()
    
    context = {
        'menulist' : menulist,
        'food' : food,
        'menu' : menu
    }

    return render_template('managemenu.html', **context)

@main.route('/addrecipe', methods=['GET', 'POST'])
@login_required
def addrecipe():
    if (current_user.role != 'Manager' and current_user.role != 'Chef' and current_user.role != 'SalesManager'):
        return redirect(url_for('main.index'))

    recipe = Recipe(
        Food_id = request.form['Food_id'],
        ingredient_supplier_id = request.form['ingredient_supplier_id']
    )
    db.session.add(recipe)
    db.session.commit()

    return redirect(url_for('main.managefoodingredients'))

@main.route('/managefoodingredients')
@login_required
def managefoodingredients():
    if (current_user.role != 'Manager' and current_user.role != 'Chef' and current_user.role != 'SalesManager'):
        return redirect(url_for('main.index'))
    ingredientsuppliers = db.session.query(Ingredientsupplier, Ingredient, Supplier)\
        .filter(Ingredient.ingredient_id == Ingredientsupplier.ingredient_id)\
        .filter(Supplier.supplier_id == Ingredientsupplier.supplier_id)\
        .all()
    food = db.session.query(Food).all()
    foodingredients = db.session.query(Food, Recipe, Ingredientsupplier, Ingredient, Supplier)\
        .filter(Food.food_id == Recipe.food_id)\
        .filter(Recipe.ingredient_supplier_id == Ingredientsupplier.ingredient_supplier_id)\
        .filter(Ingredient.ingredient_id == Ingredientsupplier.ingredient_id)\
        .filter(Supplier.supplier_id == Ingredientsupplier.supplier_id)\
        .order_by(Food.food_id)\
        .all()
    
    context = {
        'foodingredients' : foodingredients,
        'food' : food,
        'ingredientsuppliers' : ingredientsuppliers
    }

    return render_template('managefoodingredients.html', **context)

@main.route('/rateuser', methods=['GET', 'POST'])
@login_required
def rateuser():
    if (current_user.role == 'Visitor'):
        return redirect(url_for('main.index'))
        
    ratingavg = db.session.query(func.avg(Rating.rating)\
        .label('average'))\
        .filter(Rating.rater_id == current_user.id)\
        .scalar()
    ordernum = db.session.query(func.count(Order.order_id)).\
        filter(Order.user_id == current_user.id).\
        scalar()
    if (current_user.role == 'Registered'):
        if(ratingavg >= 4 and ordernum >= 3):
            user = User.query.get_or_404(current_user.id)
            user.role = 'VIP'
            db.session.commit()
        if(ratingavg <= 2 and ratingavg > 1 and ordernum >= 3):
            user = User.query.get_or_404(current_user.id)
            user.role = 'Visitor'
            db.session.commit()
        if(ratingavg == 1 and ordernum >= 3):
            user = User.query.get_or_404(current_user.id)
            user.role = 'Blacklisted'
            db.session.commit()
    rated_id = request.form['rated_id']
    rating = Rating(
        rating = request.form['rating'],
        rated_id = rated_id,
        rater_id = current_user.id
    )
    db.session.add(rating)
    db.session.commit()

    return redirect(url_for('main.rating'))

@main.route('/rating')
@login_required
def rating():
    if (current_user.role == 'Visitor' or current_user.role == 'Blacklisted'):
        return redirect(url_for('main.index'))
    user = db.session.query(User)\
        .filter(User.id != current_user.id)\
        .all()
    user2 = db.session.query(User, Order)\
        .filter(User.id != current_user.id)\
        .all()
    rating = db.session.query(Rating, User)\
        .filter(User.id != current_user.id)\
        .filter(Rating.rated_id == current_user.id)\
        .filter(Rating.rater_id == User.id)\
        .all()
    if (current_user.role == 'Registered'):
        user2 = db.session.query(User, Order)\
        .filter(User.id != current_user.id)\
        .filter(User.id == Order.user_id)\
        .order_by(Order.order_date)\
        .all()
    if (current_user.role == 'Deliverer'):
        user2 = db.session.query(User, Order)\
        .filter(User.id != current_user.id)\
        .filter(User.id == Order.deliverer_id)\
        .order_by(Order.order_date)\
        .all()
    if (current_user.role == 'Chef'):
        user = db.session.query(User)\
        .filter(User.id != current_user.id)\
        .filter(User.restaurant_id == current_user.restaurant_id)\
        .filter(User.role == 'Salesmanager')\
        .all()
    ratingavg = db.session.query(func.avg(Rating.rating)\
            .label('average'))\
            .filter(Rating.rater_id == current_user.id)\
            .scalar()
    ordernum = db.session.query(func.count(Order.order_id)).\
        filter(Order.user_id == current_user.id).\
        scalar()
    context = {
        'user' : user,
        'user2' : user2,
        'rating' : rating,
        'ratingavg' : ratingavg,
        'ordernum' : ordernum
    }

    return render_template('rating.html', **context)


@main.route('/orderfood')
@login_required
def orderfood():
    if (current_user.role == 'Registered' or current_user.role == 'VIP' and current_user.role != 'SalesManager'):
        return redirect(url_for('main.index'))
    ingredientsuppliers = db.session.query(Ingredientsupplier, Ingredient, Supplier)\
        .filter(Ingredient.ingredient_id == Ingredientsupplier.ingredient_id)\
        .filter(Supplier.supplier_id == Ingredientsupplier.supplier_id)\
        .all()
    food = db.session.query(Food).all()
    foodingredients = db.session.query(Food, Recipe, Ingredientsupplier, Ingredient, Supplier)\
        .filter(Food.food_id == Recipe.food_id)\
        .filter(Recipe.ingredient_supplier_id == Ingredientsupplier.ingredient_supplier_id)\
        .filter(Ingredient.ingredient_id == Ingredientsupplier.ingredient_id)\
        .filter(Supplier.supplier_id == Ingredientsupplier.supplier_id)\
        .order_by(Food.food_id)\
        .all()
    
    context = {
        'foodingredients' : foodingredients,
        'food' : food,
        'ingredientsuppliers' : ingredientsuppliers
    }

    return render_template('managefoodingredients.html', **context)