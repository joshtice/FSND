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

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after 
         completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authoization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    """

    @app.route("/categories", methods=["GET"])
    def categories():
        categories = [category.type for category in Category.query.all()]
        return jsonify({"categories": categories})

    """
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    """

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

    """
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be 
    removed.
    This removal will persist in the database and when you refresh the page. 
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify(question.format())
        except:
            abort(422)

    """
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    """

    @app.route("/add", methods=["POST"])
    def add_question():
        submission = request.json
        try:
            new_question = Question(**submission)
            new_question.insert()
            return jsonify(new_question.format())
        except:
            abort(422)

    """
    `@TODO: 
    `Create a POST endpoint to get questions based on a search term. 
    `It should return any questions for whom the search term 
    `is a substring of the question. 

    `TEST: Search by any phrase. The questions list will update to include 
    `only question that include that string within their question. 
    `Try using the word "title" to start. 
    `"""

    @app.route("/questions", methods=["POST"])
    def search_questions():
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
        except:
            abort(422)

    """
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    @app.route("/categories/<int:category>/questions")
    def category_questions(category, methods=["GET"]):
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

    """
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

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
        except:
            abort(422)

    """
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    """

    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({"success": False, "error": 404, "message": "Not found"}), 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Not processable"}),
            422,
        )

    return app
