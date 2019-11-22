# Full Stack API Final Project

## Description

This project was completed as part of Udacity's Fullstack Developer Nanodegree. 
The objective was to provide an API to drive the frontend of a Trivia web
application. Users of the app have the capability to:

1) Display questions by category
2) Delete questions
3) Add questions
4) Search for questions
5) Play the quiz game with a randomized sequence of questions

## Getting Started

### Setting up the Backend

#### Installing Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Setting Up a Virtual Enviornment

We recommend working within a virtual environment. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies for the Backend

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

#### Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Setting up the Frontend

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

### Running Tests

To run the tests, run the following from the backend directory:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started

- Base URL: This app is only intended to be run locally at present. The backend is accessible at the default URL: http://127.0.0.1:5000/
- Authentication: This version of the app does not require authentication

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "Not found"
}
```

Two error types are possible: 
- 400: Resource not found
- 422: Request not processable

### Endpoints

#### GET /categories
- General: Returns the categories of questions supported by the quiz api
- Example: ```curl http://127.0.0.1:5000/categories```
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ]
}
```

#### GET /questions
- General: Returns a list of questions, paginated in groups of 10
- Example ```curl http://127.0.0.1:5000/questions&page=2```
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "totalQuestions": 17
}
```

DELETE /questions/<question_id>
- General: Delete a question from the database with a certain question id
- Example: ```curl -X DELETE http://127.0.0.1:5000/questions/23```
```
{
  "answer": "Scarab", 
  "category": 4, 
  "difficulty": 4, 
  "id": 23, 
  "question": "Which dung beetle was worshipped by the ancient Egyptians?"
}
```

POST /add
- General: Add a new question to the database
- Example: ```curl -X POST -H "Content-type: application/json" -d '{"question": "Which martial art was developed in Brazil by the Gracie family?", "answer": "Brazilian Jiu Jitsu", "category": 6, "difficulty": 4}' http://127.0.0.1:5000/add```
```
{
  "answer": "Brazilian Jiu Jitsu", 
  "category": 6, 
  "difficulty": 4, 
  "id": 24, 
  "question": "Which martial art was developed in Brazil by the Gracie family?"
}
```

POST /questions
- General: Search for a question based on a search term
- Example: ```curl -X POST -H "Content-type: application/json" -d '{"searchTerm": "soccer"}' http://127.0.0.1:5000/questions```
```
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "total_questions": 2
}
```

GET /categories/<category_id>/questions
- General: Fetch all questions in a given category
- Example: ```curl http://127.0.0.1:5000/categories/1/questions```
```
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": 3, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "totalQuestions": 3
}
```

POST /quizzes
- General: Fetch a random question to play the quiz
- Example: ```curl -X POST -H "Content-type: application/json" -d '{"previous_questions": [], "quiz_category": {"id": 4}}' http://127.0.0.1:5000/quizzes```
```
{
  "question": {
    "answer": "Maya Angelou", 
    "category": 4, 
    "difficulty": 2, 
    "id": 5, 
    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }
}
```

## Authors
This project was completed in part by Joshua Tice, with significant contributions from the team at Udacity

## Acknowledgements
Many thanks to Udacity for the starter code for this project