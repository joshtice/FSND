import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    random.seed(42)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authoization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories", methods=["GET"])
    def categories():
        categories = [category.type for category in Category.query.all()]
        return jsonify({"categories": categories})

    @app.route("/questions")
    def questions(methods=["GET"]):
        questions = [question.format() for question in Question.query.all()]
        total_questions = len(questions)
        categories = [category.type for category in Category.query.all()]
        page_num = request.args.get("page", 1, type=int)
        start_index = (page_num - 1) * QUESTIONS_PER_PAGE
        end_index = min(len(questions), page_num * QUESTIONS_PER_PAGE)
        return jsonify(
            {
                "questions": questions[start_index:end_index],
                "totalQuestions": total_questions,
                "current_category": 1,
                "categories": categories,
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify(question.format())
        except Exception:
            abort(422)

    @app.route("/add", methods=["POST"])
    def add_question():
        submission = request.json
        try:
            new_question = Question(**submission)
            new_question.insert()
            return jsonify(new_question.format())
        except Exception:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def search_questions():
        if "searchTerm" not in request.json.keys():
            abort(422)

        try:
            query = request.json["searchTerm"].lower()
            hits = Question.query.filter(
                func.lower(Question.question).contains(query)
            ).all()
            questions = [question.format() for question in hits]
            return jsonify(
                {
                    "questions": questions,
                    "total_questions": len(hits),
                    "current_category": 1,
                }
            )
        except Exception:
            abort(422)

    @app.route("/categories/<int:category>/questions")
    def category_questions(category, methods=["GET"]):
        if Category.query.filter_by(id=category).first() == None:
            abort(404)

        questions = [
            question.format()
            for question in Question.query.filter_by(category=category).all()
        ]
        total_questions = len(questions)
        categories = [category.type for category in Category.query.all()]
        return jsonify(
            {
                "questions": questions,
                "totalQuestions": total_questions,
                "current_category": category,
                "categories": categories,
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def quizzes():
        try:
            previous_question_ids = request.json["previous_questions"]
            category_id = request.json["quiz_category"]["id"]
            if int(category_id) > 0:
                questions = (
                    Question.query.filter(Question.category == category_id)
                    .filter(~Question.id.in_(previous_question_ids))
                    .all()
                )
            else:
                questions = Question.query.all()
            if not questions:
                return jsonify({})
            else:
                question = random.choice(questions)
                return jsonify({"question": question.format()})
        except Exception:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404)

    @app.errorhandler(405)
    def not_allowed(error):
        return (jsonify({
            "success": False,
            "error": 405,
            "message": "Not allowed",
        }), 405)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            "success": False,
            "error": 422,
            "message": "Not processable"
        }), 422)

    return app
