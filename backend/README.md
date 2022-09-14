# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash


```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

POST /categories

This adds a category to the collection of categories in the database. It takes in category type it takes no query parameter

type: string (required) - Category type

{"type": "Entertainment"}

Sample Request

curl http://localhost:5000/categories -X POST -H "{Content-Type: 'application/json'}" -d '{"type": "Entertainment"}'
Sample Response

added: int - Id of the added category.
success: boolean - Request success status.

{
"added": 1,
"success": True
}

GET /categories/{category_id}/questions

Fetches a dictionary of questions for the specified category

{
"questions": [
{
"answer": "Alexander Fleming",
"category": 1,
"difficulty": 4,
"id": 10,
"question": Who discovered penicillin?"
},
{
"answer": "Uruguay",
"category": 6,
"difficulty": 4,
"id": 11,
"question": "Which country won the first ever soccer World Cup in 1930?"
}
],
"totalQuestions": 2
}

Questions
GET /questions

This returns a paginated list of all questions within the database. Each page contains a maximum of 10 questions.

{
"questions": [
{
"answer": "Brazil",
"category": 6,
"difficulty": 3,
"id": 10,
"question": "Which is the only team to play in every soccer World Cup tournament?"
}, {
"answer": "Uruguay",
"category": 6,
"difficulty": 4,
"id": 11,
"question": "Which country won the first ever soccer World Cup in 1930?"
}
],
"categories" : {
"1": "Science",
"2", "Art",
"3": "History"
},
"totalQuestions": 2
}

POST /questions

This adds a question to the collection of questions in the database.

{
"question": "Which country won the first ever soccer World Cup in 1930?",
"answer": "Uruguay",
"category": 6,
"difficulty": 4
}

POST /questions (SEARCH)

This performs a case insensitive search of questions from the database based on a search term. It returns an array of the questions and the total amount of questions that match the search term.

{ "searchTerm": "soccer"}
Request

Response

{
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
"totalQuestions": 2
}

DELETE /questions/{question_id}

This deletes the question with the specified id. It returns the id of the deleted question and a success status.

{
"deleted": 1,
"success": True
}

Quizzes
POST /quizzes

This returns a random question from the database within a specified category or from a random category if none is specified. It accepts an array of previous questions to ensure that a question that has been chosen before is not chosen again.

{
"previous_questions": [10],
"quiz_category": 6
}

{
"question": {
"answer": "Uruguay",
"category": 6,
"difficulty": 4,
"id": 11,
"question": "Which country won the first ever soccer World Cup in 1930?"
},
}

Leaderboard
GET /leaderboard

This returns a paginated list of all players and their scores in the database. Each page contains a maximum of 10 results.

{
"results": [
{
"id": 1,
"player": "Londy",
"score": 5,
}, {
"id": 10,
"player": "Mbuso",
"score": 4,
}
],
"totalResults": 2
}

POST /leaderboard

This adds a player's name and score to the database.

{
"player": "Londy",
"score": 4
}

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Errors re returned as JSON in the following format:
{
"error": 404,
"message": "The requested resource was not found."
}

Response Keys

error - Status code of the error that occurred.
message - Accompanying error message.

Status Codes

400 (Bad request) - Your request was not properly formatted.
404 (Not found) - The requested resource was not found.
422 (Unprocessable) - The server understood your request but it could not be processed.
500 (Internal server error) - Something went wrong on the server.
