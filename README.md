# Rest_api - Person Management System

This is a **Django-based REST API** project called **Rest_api** that allows for managing `Person` data. It provides functionalities for **user registration**, **login**, and **CRUD operations** on `Person` records. The project also supports **pagination**, **search functionality**, and **token-based authentication** for secured API access. The API is fully documented using **Swagger UI**.

## Features

- **User Registration**: Allows new users to register an account.
- **User Authentication**: Users can log in to get an authentication token.
- **CRUD Operations for Person**: Create, retrieve, update, and delete `Person` records.
- **Custom Pagination**: Paginate the list of persons, configurable via query parameters.
- **Search Functionality**: Search for persons by name.
- **Swagger UI**: Interactive API documentation to explore and test the API.
- **Token Authentication**: API access is secured using token authentication.

## Technologies Used

- **Django**: Web framework for building the API.
- **Django REST Framework (DRF)**: For building RESTful APIs.
- **DRF Spectacular**: For generating OpenAPI schema and Swagger UI.
- **SQLite**: Default database (can be replaced with PostgreSQL or MySQL).
- **Token Authentication**: For securing API endpoints.

## Installation

Follow these steps to set up and run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Rest_api.git
cd Rest_api
```
### 2. Install dependencies
  Make sure you have Python 3.x installed. Then, install the required Python packages:

```bash
pip install -r req.txt
```
### 3. Set up the database
By default, the project uses SQLite, but you can configure other databases like PostgreSQL if needed. Run the following commands to apply the migrations and set up the database:

```bash
python manage.py migrate
```
### 4. Create a superuser (optional)
To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```
### 5. Run the development server
Start the Django development server:

```bash
python manage.py runserver
```
The API will be available at http://127.0.0.1:8000.



### Documentation Endpoints
  GET /swagger/: Interactive API documentation via Swagger UI. You can test all the endpoints interactively here.


  Permissions and Authentication
  - **IsAuthenticated**: Most endpoints require the user to be authenticated. You need to provide the authentication token in the request headers.
  
    AllowAny: The /register/ and /login/ endpoints are open to anyone.
  
  - **Authentication** is handled using Token Authentication. Once a user logs in, they receive a token that must be included in the request headers as Authorization: Token <your_token> for accessing protected endpoints.
  
  - **Custom Pagination**
    The project supports custom pagination using the PageNumberPagination class:
    
    Default page size is 10.
    
    Clients can adjust the page size using the page_size query parameter (up to a maximum of 100).
    
    Example: GET /persons/?page=2&page_size=20

### API Documentation
  This project uses drf-spectacular to generate the OpenAPI schema and provides interactive API documentation via Swagger UI.
  
  To view the Swagger UI:
  
  GET /swagger/: View the interactive documentation.

### Testing
  Run tests with Django's built-in test framework:
  
  ```bash
  python manage.py test
