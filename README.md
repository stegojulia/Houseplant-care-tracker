# Houseplants care app
The idea for this project was born when I was looking for a system to track the care of my collection of plants. Tracking of activities such as watering, fertilising and repotting is useful because it allows a gardener to gather data about the plants to learn more about their care, ensure that plants are not overwatered or overfertilised, and facilitates producing accurate care instructions, for example if I had to travel and need someone else to look after my collection.

# Design

## Project specification
This project's objective is to create a CRUD web application with Python and Flask. The project aimed to demonstrate proficiency in a range of concepts and skills, including:

* Project Management
* Python Fundamentals
* Python Testing
* Git
* Basic Linux
* Python Web Development
* Continuous Integration
* Cloud Fundamentals
* Databases

## Scope
An important aspect of the project was to adjust the level of complexity of the app to fit into the scope of the project. This required brainstorming any possible functions and prioritising the essential ones. Two key elements emerged:
* Storing general information about plants, which can be updated and deleted if required
* Storing information about the watering schedule

## Database design
The essential elements of the database were established in advance and visualised with an ERD chart, which demonstrates the relationship between the tables. Additional tables can be added in the future as more features are added to the app. The ERD was designed with Lucidchart.

<img src="Images/Houseplant Tracker - QA Project_1.png" alt="ERD" style="width:20;">


# Project management

## Workflow
A Trello board was the main project management tool used. The board developed along with the project as my knowledge increased. Initially, it only included user stories with main features. Later I was able to decompose each story into smaller tasks. In addition to the MVP elements, I also added additional tasks which can be carried out to expand the app. I updated the board daily. Several times it became clear that what I initially thought was essential was not as important - and vice versa, so I adjusted the plan accordingly.

<img src="Images/trello" alt="Trello-board" style="width:20;">

## CI Pipeline

## Risk assessment


<img src="Images/risk-assessment-matrix.png" alt="risk assessment matrix" class="center" style="width:20;">

<img src="Images/risk-assessment-list.png" alt="risk assessment list" class="center" style="width:20;">

## Unit testing

Unit testing with Pytest was implemented for automated testing of the CRUD functionality. A coverage of 80% was achieved.

<img src="Images/unit-test.png" alt="risk assessment list" class="center" style="width:20;">


## Challenges and solutions

## What I would have done differently

## Possible additions and improvements

* Search bar.
* More care features (fertilising, repotting, pruning, pest control).
* Adding images representing the plants and their condition.
* Editable fields to customise the information that can be entered in the plant records.
* Predicting houseplants to be watered soon based on past watering frequency.
* Mobile app.

## Versions
v.1.0 includes a basic version of the watering feature. It enables the user to 'water' a plant (i.e. add a watering record linked to the record of a houseplant) with one click of the button. The watering date is assumed to be today's date, and the last watering date becomes visible in the plant record.

v.2.0 adds a more advanced watering feature, which allows the user to backdate waterings and view as well as edit past waterings in case of a user error.