import json
import os
import subprocess
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

def refresh_test_db():
    try:
        subprocess.run(["dropdb", "trivia_test"])
    except:
        pass
    subprocess.run(["createdb", "trivia_test"])
    subprocess.run(["psql", "trivia_test", "-f", "trivia.psql"])

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_categories(self):
        expected = {
            "categories": [
                "Science",
                "Art",
                "Geography",
                "History",
                "Entertainment",
                "Sports",
            ]
        }
        response = self.client().get("/categories")
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    def test_questions(self):
        expected = {
            "categories": [
                "Science",
                "Art",
                "Geography",
                "History",
                "Entertainment",
                "Sports",
            ],
            "current_category": 1,
            "questions": [
                {
                    "answer": "Maya Angelou",
                    "category": 4,
                    "difficulty": 2,
                    "id": 5,
                    "question": "Whose autobiography is entitled 'I Know Why the "
                    "Caged Bird Sings'?",
                },
                {
                    "answer": "Muhammad Ali",
                    "category": 4,
                    "difficulty": 1,
                    "id": 9,
                    "question": "What boxer's original name is Cassius Clay?",
                },
                {
                    "answer": "Apollo 13",
                    "category": 5,
                    "difficulty": 4,
                    "id": 2,
                    "question": "What movie earned Tom Hanks his third straight "
                    "Oscar nomination, in 1996?",
                },
                {
                    "answer": "Tom Cruise",
                    "category": 5,
                    "difficulty": 4,
                    "id": 4,
                    "question": "What actor did author Anne Rice first denounce, "
                    "then praise in the role of her beloved Lestat?",
                },
                {
                    "answer": "Edward Scissorhands",
                    "category": 5,
                    "difficulty": 3,
                    "id": 6,
                    "question": "What was the title of the 1990 fantasy directed "
                    "by Tim Burton about a young man with multi-bladed "
                    "appendages?",
                },
                {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer "
                    "World Cup tournament?",
                },
                {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup "
                    "in 1930?",
                },
                {
                    "answer": "George Washington Carver",
                    "category": 4,
                    "difficulty": 2,
                    "id": 12,
                    "question": "Who invented Peanut Butter?",
                },
                {
                    "answer": "Lake Victoria",
                    "category": 3,
                    "difficulty": 2,
                    "id": 13,
                    "question": "What is the largest lake in Africa?",
                },
                {
                    "answer": "The Palace of Versailles",
                    "category": 3,
                    "difficulty": 3,
                    "id": 14,
                    "question": "In which royal palace would you find the Hall of "
                    "Mirrors?",
                },
            ],
            "totalQuestions": 19,
        }

        response = self.client().get("/questions")
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)

    def add_question(self):
        data = {
            "question": "test question",
            "answer": "test answer",
            "difficulty": 1, 
            "category": 1,
        }
        expected = {
            "id": 24,
            "question": "test question",
            "answer": "test answer",
            "difficulty": 1, 
            "category": 1,
        }
        response = self.client().post(
            "/add",
            data=json.dumps(data),
            content_type="application/json"
        )
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)
    
    def delete_question(self):
        expected = {
            "id": 24,
            "question": "test question",
            "answer": "test answer",
            "difficulty": 1,
            "category": 1,
        }
        response = self.client().delete(
            "questions/24"
        )
        result = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, expected)
    
    def test_add_delete(self):
        self.add_question()
        self.delete_question()
    


# Make the tests conveniently executable
if __name__ == "__main__":
    refresh_test_db()
    unittest.main()
