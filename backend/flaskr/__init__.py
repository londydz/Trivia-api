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


def standalone_print(item):
    print("\n\n", item, "\n\n")


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
    def get_categories():

        selection = Category.query.all()
        current_categories = {
            category.id: category.type for category in selection}

        return jsonify(
            {
                "success": True,
                "categories": current_categories
            }
        )

    @app.route("/categories", methods=["POST"])
    def add_category():

        try:
            type = request.get_json()["type"]
            category = Category(type=type)
            category.insert()

            return jsonify({
                "success": True,
                "created": category.id,

            })
        except BaseException:
            abort(400)

    @app.route("/questions")
    def get_questions():

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
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
    def add_question():

        body = request.get_json()

        question = body.get('Question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        searchTerm = body.get('searchTerm', None)

        try:

            if searchTerm:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(searchTerm)))
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions.all()),
                    'current_category': None
                })
            else:
                question = body["question"]
                answer = body["answer"]
                difficulty = int(body["difficulty"])
                category = int(body["category"])

                question = Question(
                    question=question,
                    answer=answer,
                    difficulty=difficulty,
                    category=category,
                )

                question.insert()

                return jsonify({
                    "success": True,
                    "added": question.id,

                })

        except Exception:
            abort(400)

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_in_category(category_id):
        '''
          Endpoint to get questions based on category.
        '''
        questions = Question.query.filter_by(category=category_id).all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_Questions": len(current_questions),
            "current_Category": None,
        })

    @app.route("/quizzes", methods=["POST"])
    def get_question_for_quiz():

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

    @app.route("/leaderboard")
    def get_leaderboard_scores():

        scores = Leaderboard.query.order_by(desc(Leaderboard.score)).all()
        paginated_results = paginate_questions(request, scores)
        return jsonify({
            "results": paginated_results,
            "total_Results": len(scores)
        })

    @app.route("/leaderboard", methods=["POST"])
    def post_to_leaderboard():
        '''
          Endpoint to add a new category.
        '''
        try:
            player = request.get_json()["player"]
            score = int(request.get_json()["score"])

            item = Leaderboard(player=player, score=score)
            item.insert()

            return jsonify({
                "added": item.id,
                "success": True
            })
        except BaseException:
            abort(400)

    '''
      Error handlers for all expected errors
    '''

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"}),

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify(
            jsonify({"success": False, "error": 500,
                    "message": "internal server error"}),
            500,
        )

    return app
