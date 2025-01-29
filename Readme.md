## Employees Management Application Setup Guide

This guide provides comprehensive instructions for setting up and using your this Flask application, including installing dependencies, setting up the database, running tests, and testing the API using Postman or other test applications.

# Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Virtual Environment Setup](#virtual-environment-setup)
    - [Installing Packages](#installing-packages)
- [Database Setup](#database-setup)
    - [Running Tests](#running-tests)
    - [Testing the API](#testing-the-API)
- [Usage](#usage)


## Prerequisites
Before you begin, ensure you have the following installed on your machine:

```
    Python 3.x

    MySQL
```

## Installation
### Virtual Environment Setup
On Windows
Open Command Prompt or PowerShell.

Navigate to your project directory.

Create a virtual environment:

```
    python -m venv venv
```
Activate the virtual environment:
```
    venv\Scripts\activate
```
On Linux/MacOS
Open Terminal.

Navigate to your project directory.

Create a virtual environment:

```
    python3 -m venv venv
```
Activate the virtual environment:

```
    source venv/bin/activate
```
### Installing Packages
Remember to set up .env file with FLASK_DATABASE_URI and FLASK_SECURITY_KEY for flask jwt extended
With the virtual environment activated, install the required packages from requirements.txt:

```
    pip install -r requirements.txt
```

## Database Setup
MySQL Setup
Make sure that MySQL server is running on your machine.
Configure your Flask application to use the MySQL database by adding the following to your .env file:

```SQLALCHEMY_DATABASE_URI=mysql://<username>:<password>@localhost/database_name```
Initialize the database:
Navigate to terminal and run this command: ```flask shell```
Before running the above make sure you have exported flask application environment variable

Before running the code bellow, make sure you have import db in the flask shell
When terminal opens up, run this command to create database tables: ```db.create_all()```


## Running Tests
Using Flask-Testing
To run the tests using Flask-Testing, execute the following command:

```python -m tests.test_cases```
Ensure that your test files are located in the tests directory and follow the naming convention.

## Testing the API
### Using Postman
You must create use profile before making POST, PUT or DELETE request. Thus, following the bellow instruction, create your user profile first with **email** and **password**. After creating it, you can create employee and the rest of crud operations.
1. Open Postman.

2. Create a new request.

3. Set the request method (GET, POST, PUT, DELETE).

4. Enter the request URL
    for employees http://localhost:5000/employee/1  
    for auth http://localhost:5000/register/ or http://localhost:5000/login/  
    for users http://localhost:5000/users/ 

6. Set the request headers, including the Authorization header for JWT token.

7. Set the request body (if applicable) in form-data format.

8. Send the request and verify the response.

## Usage
Remember to use set request type as form-data

**Description:**
This endpoint registers a new user.

**Request:**
POST /register
```
    {
      "email": "email@example.com",
      "password": "your_password"
    }
```
**Response:**
```
    {
      "message": "Account created successfully"
    }
```

POST /login
```
    {
      "email": "user@example.com",
      "password": "password"
    }
```

**Response**:

```
    {
      "access_token": "your_jwt_token"
    }
```
