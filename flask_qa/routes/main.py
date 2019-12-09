from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

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

@main.route('/managesalesorder')
@login_required
def managesalesorder():
    if not (current_user.role == 'Salesmanager'):
        return redirect(url_for('main.index'))

    salesorderlist = db.session.query(Supplyorder, Ingredientorder)\
        .filter(Supplyorder.supply_order_id == Ingredientorder.supply_order_id)\
        .filter(Supplyorder.restaurant_id == current_user.restaurant_id)\
        .filter(Supplyorder.approval == False)\
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