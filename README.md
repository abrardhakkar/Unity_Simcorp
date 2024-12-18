# Unity_Simcorp

SimCorp School Project
This repository contains a school project developed as part of my studies, where I worked on building a web application using Python and MySQL. The project demonstrates my skills in backend development, database management, and web applications.

Content
Code Files: Python scripts for server logic and database interaction.
Database: MySQL database for handling and storing data.
Web Application: Flask-based application acting as a simple "homepage".
Technologies
Python: Used for backend development.
Flask: Web framework for application logic and routing.
MySQL: Database for data storage and queries.
HTML/CSS: Simple front-end design.
Features
User Authentication: Login and registration system with hashed passwords (SHA256).
Dashboard: A dynamic page where users can view their data.
Portfolio Management: Ability to add, view, and delete trade data.
Stock Analysis: Integration with Yahoo Finance API to fetch stock data and visualize it using graphs.
JSON Format: A requirement was to convert the data to JSON format to add volume and showcase efficient data processing.
API Integration: Emphasis on using and integrating APIs to extend application functionality.
How to Run the Project
Clone the repository:

git clone <repository-link>
cd <repository-folder>
Set up a virtual environment:

python -m venv venv
source venv/bin/activate # (Windows: venv\Scripts\activate)
Install dependencies:

pip install -r requirements.txt
Configure the database:

Ensure MySQL is installed and running.
Import the database from the included family_office.sql file:
mysql -u root -p family_office < family_office.sql
Run the application:

python app.py
Open the browser: Navigate to http://127.0.0.1:5000 to use the application.

Project Structure
app.py: The main file that starts the Flask application.
mysqlConnect.py: Contains database connection functionality.
endpoints.py: Contains all API endpoints and business logic.
templates/: Contains HTML files for the user interface.
Learning Outcomes
Effective use of Flask to build a RESTful backend.
Integration with MySQL database for efficient data storage.
Implementation of user authentication with password hashing.
Use of external APIs (Yahoo Finance) for stock analysis.
Conversion of data to JSON format to meet project requirements and ensure easy data exchange.
Focus on API integration to enhance application features and usability.
Contact
If you have any questions or would like further information about the project, feel free to contact me at m.abrarparwez@gmail.com.
