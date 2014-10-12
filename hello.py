import os
import random

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


from forms import AddEntryForm
from models import Expression

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
	data = request.form
	results = []
	for key in data:
		entry = Expression.query.filter_by(id=key).one();
		user_input = data[key]
		entry = entry.__dict__
		entry['user_input'] = user_input
		entry['error'] = user_input != entry['swedish']
		results.append(entry)
        results = sorted(results, key=lambda expression: expression['id'] )
    	return render_template('results.html', entries=results)

    all_entries = Expression.query.order_by(Expression.id).all()
    entries = random.sample(all_entries, 5)
    entries = sorted(entries, key=lambda expression: expression.id )
    return render_template('entries.html', entries=entries)

@app.route('/addentry', methods=['GET', 'POST'])
def addentry():
    form = AddEntryForm(request.form)
    if request.method == 'POST' and form.validate():
	finnish = form.finnish.data
        swedish = form.swedish.data
        expression = Expression(finnish, swedish) 
        db.session.add(expression)
        db.session.commit()
        form = AddEntryForm()
        return render_template('addentry.html', form=form, success=True)
    return render_template('addentry.html', form=form)



