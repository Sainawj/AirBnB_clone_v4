# Airbnb Clone
This project is a clone of the AirBnB platform, implemented using Flask. It includes several components such as console interaction, web static files, MySQL integration, RESTful API, load balancing, and web infrastructure design

![Screenshot](airbnb.jpg)

## Features 
1. The console: Interactive console for managing the application.
2. Web static: HTML, CSS, and JavaScript static files for the frontend.
3. MySQL: MySQL database integration for data management.
4. Deploy static: Deployment of static web files.
5. Web framework: Flask for managing HTTP requests.
6. RESTful API: Provides API endpoints for CRUD operations.
7. Web dynamic: Dynamic web pages using AJAX for an interactive user experience.
8. Load balancer: Distributes traffic between multiple servers for high availability.
9. Web infrastructure design: Architecture optimized for scalability and security.

## Requirements
* Python 3.x
* Flask
* MySQL
* SQLAlchemy
* Gunicorn (for deployment)
* Nginx (for load balancing)
* Virtualenv

## Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/sainawj/airbnb_clone_v4.git
    cd airbnb_clone_v4
  
  2. **Install Dependencies**
     ```bash
     pip install -r requirements.txt
  3. **Set Up a Virtual Environment**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
5. **Install MySQL Server**
   ```bash
   sudo apt-get update
   sudo apt-get install mysql-server
   sudo mysql_secure_installation ##secure your MySQL setup

6. **Create a MySQL Database**
   ```bash
   mysql -u root -p
   CREATE DATABASE airbnb_clone;
7. **Set Up Environment Variables**
   Create a .env file with your database credentials:
   ```makefile
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=mysql+pymysql://root:rootpassword@localhost/airbnb_clone
8. **Initialize the Database**
   Run migrations to set up the database tables:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
9. **Start the Flask Application**
    Run the app with:
    ```bash
    flask run


The application will be available at http://127.0.0.1:5000.
