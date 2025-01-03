# Todo App with Django Rest Framework and JWT Authentication and Email verification

This is a Todo application built using Django Rest Framework (DRF) and JSON Web Token (JWT) authentication. The application allows users to create, update, delete, and view their todos.


## Installation

To install and run this project, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment and activate it.
4. Install the required dependencies by running `pip install -r requirements.txt`.
5. Set .env file with your PostgreSQL and Email credentials.
6. Run `python manage.py runserver` to start the server.

## Usage

Once the server is running, you can use the API endpoints to interact with the application. The API uses JWT authentication, so you will need to obtain a token before making requests to protected endpoints.


## Docker:
1. 
   ```
   docker compose up --build
   ```
2. 
   ```
   docker compose run python manage.py migrate
   ```


## Features

- User authentication with JWT
- Create, update, delete, and view todos
- Email verification
- Persistent data storage with PostgreSQL

## Technologies

- Django
- Django Rest Framework
- Django Rest Framework Simple JWT
- PostgreSQL

## Contributing

Contributions are welcome! Please submit a pull request or open an issue.

