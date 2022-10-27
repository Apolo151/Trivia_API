import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# defining a function to paginate questions for a page
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    return questions[start:end]


# defining a function to format categories for the frontend
def format_categories(categories):
    categories_dict = {}
    for category in categories:
        categories_dict[category.id] = category.type
    return categories_dict


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type , Authorization')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

    @app.route("/categories")
    def get_categories():
        # get all categories from the database
        selection = Category.query.order_by(Category.id).all()
        # format the categories
        categories = format_categories(selection)
        return jsonify({
          'success': True,
          'categories': categories
        })

    @app.route("/questions")
    def get_paginated_questions():
        # get all categories from the database
        categories_selection = Category.query.order_by(Category.id).all()
        # format the categories
        categories = format_categories(categories_selection)
        # get all questions from the databse
        questions = Question.query.order_by(Question.id).all()
        # paginate to get current page questions
        current_questions = paginate_questions(request, questions)
        # if there is no questions for the requested page return an error
        if current_questions == []:
            abort(404)
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(questions),
          'categories': categories,
          'current_category': None
        })

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            # get the question by id
            question = Question.query.filter(
              Question.id == question_id).one_or_none()
            # else delete the question from the database
            question.delete()
            return jsonify({
              'success': True,
              'deleted': question.id,
            })
        except:
            abort(404)

    @app.route("/questions", methods=['POST'])
    def add_question_or_search():
        try:
            # get the request json data
            body = request.get_json()
            search_term = body.get('searchTerm')
            # if the post request contained a searchTerm
            # search in questions by it
            if search_term:
                selection = Question.query.order_by(
                  Question.id).filter(Question.question.ilike(
                    '%{}%'.format(search_term))).all()
                # paginate the result questions
                questions = paginate_questions(request, selection)
                return jsonify({
                  'success': True,
                  'questions': questions,
                  'total_questions': len(selection),
                  'current_category': None
                })
            # else if there is no searchTerm then it is a question submission
            else:
                # if question field was left empty or
                # it was a search request but with an empty string return an
                # error
                if body['question'] == '':
                    abort(422)
                question = body['question']
                answer = body['answer']
                category = body['category']
                difficulty = body['difficulty']
                # create a new Question with the request data
                new_question = Question(
                  question=question, answer=answer,
                  category=category, difficulty=difficulty)
                # insert the new question to the database
                new_question.insert()
                # return success and the created question id
                return jsonify({
                  'success': True,
                  'created': new_question.id
                })
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def get_category_questions(category_id):
        # get the request category by id
        current_category = Category.query.filter(
            Category.id == category_id).one_or_none()
        # check if the request category doesnot exist
        if current_category is None:
            abort(404)
        # get all category questions
        category_questions = Question.query.order_by(
          Question.id).filter(Question.category == category_id).all()
        # check if there are no questions for the category
        if category_questions is None:
            abort(404)
        # paginate questions
        questions = paginate_questions(request, category_questions)
        return jsonify({
          'success': True,
          'questions': questions,
          'total_questions': len(category_questions),
          'current_category': current_category.format()
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # getting the quiz request data
        body = request.get_json()
        if body is None:
            abort(400)
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        category = quiz_category['id']
        # if user choose all get all questions
        if category == 0:
            questions = Question.query.all()
        # else get all choosen category questions
        else:
            questions = Question.query.filter(
              Question.category == category).all()
        # check if category doesn't exist
        if len(questions) == 0:
            abort(400)
        questions_num = len(questions)
        # for every question in questions ,
        # if questions id is in previous_questions,
        # set the question to None
        for i in range(questions_num):
            if questions[i].id in previous_questions:
                questions[i] = None
        # then delete all None incidents in the questions list
        # to make random.choice() choose from new questions only
        for i in range(questions_num):
            if None in questions:
                questions.remove(None)
        # if length of questions equals 0 therefore there are no new questions
        # so set question to None
        if len(questions) == 0:
            question = None
        # else get a random question from new questions
        else:
            random_question = random.choice(questions)
            question = random_question.format()

        return jsonify({
          'success': True,
          'question': question
        })

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request'
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'internal server error'
        }), 500

    return app
