
from flask import Flask, render_template, redirect, url_for, session, request
import json
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from plotlydash.dashboard import dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import string
import random

server = Flask(__name__)



# Flask-WTF requires an encryption key - the string can be anything
server.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(server)

dash_app = dash.Dash(
    server=server,
    routes_pathname_prefix='/dashboard/',
    external_stylesheets=[
        'https://fonts.googleapis.com/css?family=Lato'
    ],
    name='dash-app-1',
)

dash_app.layout = html.Div()


class NameForm(FlaskForm):
    name = StringField('Enter the link of the CSV you want to visualize', validators=[DataRequired()])
    submit = SubmitField('Submit')


@server.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        # empty the form field

        messages = json.dumps({"dataFrame":name})
        session['messages'] = messages

        form.name.data = ""
        # redirect the browser to another route and template
        print(messages)
        global server

        with server.test_request_context('/dashboard/'):
            server = dashboard(server, messages, dash_app)
        print(url_for('/dashboard/' , id = messages))
        return redirect( url_for('/dashboard/' , id = messages))
    return render_template('index.html',  form=form, message=message)


if __name__ == '__main__':  
    server.run(host='0.0.0.0')

