# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of 10 questions for the page, total number of questions, dictionary of all categories and the current category
- Request Arguments: page(type:integer, default:1): dictates the page of questions the user requests
- Returns a JSON object in the following format:
{
    'success' : True,
    'questions' : current page questions, (type: list)
    'total_questions' : total number of questions, (type: integer)
    'categories' :  all categories, (type: dictionary)
    'current_category' : current category (type: JSON(formatted category) or None)
}

DELETE '/questions/<int:question_id>'
- Deletes a question using question id
- Path parameters: question_id, the id of the question that you want to delete
- Returns a JSON object in the following format:
{
    'success': True,
    'deleted': deleted question id (type: integer)
}

POST '/questions'
- if the request is a search it searches for questions using the search term provided, 
it returns all questions for whom the search term is a substring of the question
- Request body: 
{
    'searchTerm': search term (type: string)
}
- Returns a JSON object in the following format:
{
    'success': True,
    'questions': the result questions paginated, (type: list)
    'total_questions': total number of result questions, (type: integer)
    'current_category': current category (type: JSON(formatted category) or None)
}
- else if the request is submitting a new question it adds the provided question to the database
- Request body:
{
    'question': the question, (type:string)
    'answer': the question's answer, (type:string)
    'difficulty': the question's difficulty (from 1 to 5) (type:integer)
    'category' the category id you want to add the question to (type:string)
}
- Returns a JSON object in the following format:
{
    'success': True,
    'created': the created question id (type: int)
}

GET '/categories/<int:category_id>/questions'
- Fetches all questions for a given category
- path parameters : category_id, the id of the category
- Returns a JSON object in the following format:
{
    'success':True,
    'questions': all category questions, (type: list)
    'total_questions': total number of category questions, (type: integer)
    'current_category': the current category (type: JSON(formatted category))
}

POST '/quizzes'
- Fetches questions to play the quiz 
- Request body:
{
    'previous_questions': IDs of previous questions of the current quiz, (type: list)
    'quiz_category': the category of the quiz (type: JSON(formatted category))
}
- Returns a JSON object in the following format:
{
    'success': True,
    'question': the fetched question (type: JSON(formatted question))
}

Error Handling
- Errors are returned as a JSON object in the following format:
{
    'success': False,
    'error': 404,
    'message': 'resource not found'
}

Error codes the API returns:
- 400 : bad request
- 404 : resource not found
- 422 : unprocessable
- 405 : method not allowed
- 500 : internal server error


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```