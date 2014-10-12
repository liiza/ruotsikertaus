import os
import random

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


from forms import AddEntryForm
from models import Expression

"""Render home page. """
@app.route('/')
def index():
    return render_template('index.html')

"""Render quiz. User sees finnish sentences and he must give swedish translation.
When requested with GET pick randomly five enrties and render to user five finnish sentences.
When requested with POST check user's answers and render the right results."""
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
	data = request.form
	results = []
        # Data is a dictionary of pairs (id, user_input)
	for key in data:
                # Fetch the entry
		entry = Expression.query.filter_by(id=key).one();
		# Transform from object to dict, so that we can add new elements
		entry = entry.__dict__	
		user_input = data[key]

		entry['user_input'] = user_input
		# Compare user_input with the right answer
		entry['error'] = user_input != entry['swedish']
		results.append(entry)

        results = sorted(results, key=lambda expression: expression['id'] )
    	return render_template('results.html', entries=results)

    all_entries = Expression.query.order_by(Expression.id).all()
    # Select randomly five enries to render.
    entries = random.sample(all_entries, 5)
    entries = sorted(entries, key=lambda expression: expression.id )
    return render_template('entries.html', entries=entries)

"""Add new entry to database. User provides a swedish and finnish translation."""
@app.route('/addentry', methods=['GET', 'POST'])
def addentry():
    form = AddEntryForm(request.form)
    # Validate form
    if request.method == 'POST' and form.validate():
	finnish = form.finnish.data
        swedish = form.swedish.data
        expression = Expression(finnish, swedish) 
        db.session.add(expression)
        db.session.commit()
        form = AddEntryForm()
        # Render user the form again with success message
        return render_template('addentry.html', form=form, success=True)
    return render_template('addentry.html', form=form)



