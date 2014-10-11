import os
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Expression

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
	data = request.form
	entries = []
	for key in data:
		entry = Expression.query.filter_by(id=key).one();
		user_input = data[key]
		entry = entry.__dict__
		entry['error'] = user_input
		entries.append(entry)
    	return render_template('results.html', entries=entries)

    entries = Expression.query
    return render_template('entries.html', entries=entries)


