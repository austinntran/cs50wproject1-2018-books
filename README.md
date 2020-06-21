# cs50wproject1

Web Programming with Python and JavaScript

I completed the project by creating a website using Flask/Python, Jinja, and Heroku Database/SQL commands.

# What's in Each File

1. static:
   - contains styles.scss and styles.css which hold the CSS and SASS code for the styling of the webpages

2. templates:
   - book.html: contains page that displays information on a specific book
   - index.html: contains home/landing page for the project and introduces the project
   - layout.html: contains main layout for each page, including the different navbar types and the footer on each page
   - login.html: contains login page with form to login
   - register.html: contains register page with form to register an account
   - search.html: contains search page with form to search for a book by author, isbn, or title; displays results of search also

3. application.py: contains python/flask code that handles the URL paths and requests to web application; executes SQL queries based on requests

4. import.py: python script to import books from books.csv into books table in database
