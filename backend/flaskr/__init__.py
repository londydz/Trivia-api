from dataclasses import dataclass
from functools import total_ordering
import os
from select import select
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import desc
from models import setup_db, Question, Category, Leaderboard

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [item.format() for item in data]

    return formatted_data[start: end]

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        '''
          Set Access-Control headers
        '''
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, PATCH, DELETE, OPTIONS")

        return response

    @app.route("/categories")
    def display_all_categories():

        categories = Category.query.order_by(Category.type).all()
        category_display = {
            category.id: category.type for category in categories
        }

        if len(category_display) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": category_display,
                "total categories": len(categories),
            }
        )

    @app.route("/categories", methods=["POST"])
    def create_new_category():

        type = request.get_json()["type"]

        try:
            category = Category(type=type)
            category.insert()

            selection = Category.query.all()
            current_categories = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "added": category.id,

            })
        except BaseException:
            abort(404)

    @app.route("/questions")
    def display_all_questions():

        questions = Question.query.all()
        question_display = paginate_questions(request, questions)

        categories = Category.query.all()
        category_display = {}
        for category in categories:
            category_display[category.id] = [category.type]

        if len(question_display) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': question_display,
            'total_questions': len(questions),
            'categories': category_display,
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question_by_question_id(question_id):
        '''
          Endpoint to DELETE question using a question ID.
        '''
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question:

            try:
                question.delete()
                questions = Question.query.order_by(Question.id).all()
                current_quizzes = paginate_questions(request, questions)

                data = Category.query.order_by(Category.id).all()
                categories = {}
                for category in data:
                    categories[category.id] = category.type

                return jsonify({
                    'success': True,
                    'questions': current_quizzes,
                    'total_questions': Question.query.count(),
                    'categories': categories,
                    'current_category': None
                })

            except BaseException:
                abort(422)

    @app.route("/questions", methods=["POST"])
    def create_new_question():

        data = request.get_json()
        new_question = data.get('question')
        new_answer = data.get('answer')
        new_difficulty = data.get('difficulty')
        new_category = data.get('category')

        if ((new_question is None) or (new_answer is None)
                or (new_difficulty is None) or (new_category is None)):
            abort(422)

        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'question_created': question.question,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except Exception:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_for_any_question():
        data = request.get_json()
        search_term = data.get('searchTerm', None)

        if search_term:
            results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in results],
                'total_questions': len(results),
                'current_category': None
            })

    @app.route("/categories/<int:category_id>/questions")
    def display_questions_category(category_id):

        question = Question.query.all()

        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except BaseException:
            abort(404)

    @app.route("/quizzes", methods=["POST"])
    def display_question_for_quiz():

        try:

            body = request.get_json()

            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(
                    Question.id.notin_(
                        (previous_questions))).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(
                    available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except BaseException:
            abort(422)

    '''
      Error handlers for all expected errors
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"}),

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "Resource Not Found"}),
            404,
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "Method Not Allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "Unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify(
            jsonify({"success": False, "error": 500,
                    "message": "Internal Server Error"}),
            500,
        )

    return app
