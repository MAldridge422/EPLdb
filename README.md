# Final Semester Project for CS4750-Fall 2017
Made by Matt, Tarun, Michael, and Tim

Made in [Django](https://www.djangoproject.com/)

Uses the SB Admin template by [Start Bootstrap](https://startbootstrap.com/template-overviews/sb-admin/)


## Development
You can run the site with ```python manage.py runserver``` ([manage.py](EPLdb/manage.py))

Make sure you create a secret.py file in [EPLdb/](EPLdb/) that defines SECRET_KEY for [settings.py](EPLdb/EPLdb/settings.py) 

In [settings.py](EPLdb/EPLdb/settings.py), set DEBUG = TRUE


## Site Structure
* League Standings

  Season's table
* Teams

  A single page, with tabs for each team
* Positions

  A single page, with tabs for each position
* Bookings

  A single page, with two tabs (red, yellow)
* Goals

  A single page with top goal scorers and a bar graph of goal scorers
* Raw Data

  A dropdown with tabs for each table(each has pagination and sortable)
