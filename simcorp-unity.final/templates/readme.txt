base.html contains the general HTML page design

it uses the Jinja statement include for the navigation bar

{% include "navigation.html" %}

it uses the Jinja statement block to extend the HTML page design

{% block content %}
{% endblock %}

index.html extends the base.html page design with specific content

{% extends "base.html" %}

Specific content for index.html is put inside the Jinja statement block

{% block content %}
{% endblock %}

The Jinja template engine will combine base.html, navigation.html and index.html

Read more about Template Inheritance in Flask:
https://flask.palletsprojects.com/en/2.0.x/patterns/templateinheritance/