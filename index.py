import os
import random
import string

from flask import Flask, render_template, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


from forms import AddEntryForm
from models import Expression, Favorites

def username_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

"""Render home page. """
@app.route('/')
def index():
    username = request.cookies.get('username')
    print "username is", username
    if not username:
        resp = make_response(render_template('index.html'))
        username = username_generator()
        resp.set_cookie('username', username)    
        return resp

    return render_template('index.html')

"""Render quiz. User sees finnish sentences and he must give swedish translation.
When requested with GET pick randomly five enrties and render to user five finnish sentences.
When requested with POST check user's answers and render the right results."""
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    username = request.cookies.get('username')
    if request.method == 'POST':
	data = request.form
	results = []
        # Data is a dictionary of pairs (id, user_input)
        if username:
            favorites = Expression.query.join(Favorites).filter_by(user_name=username).all()
        else:
            favorites = []
	for key in data:
                # Fetch the entry
		entry = Expression.query.filter_by(id=key).one();
		# Transform from object to dict, so that we can add new elements
		entry = entry.__dict__	
		user_input = data[key]
		entry['user_input'] = user_input
		# Compare user_input with the right answer
   		entry['error'] = user_input != entry['swedish']
                for fav in favorites:
                    if int(key) == int(fav.id):
                        entry['class'] = 'saved'
     
              	results.append(entry)

        results = sorted(results, key=lambda expression: expression['id'] )
    	return render_template('results.html', entries=results)

    # Let filter out all entries that user hasn't marked to his favorites
    entries = Expression.query.all()
    entries_to_filter = Expression.query.join(Favorites).filter_by(user_name=username).all()
    copy_entries = []
    for entry in entries:
        if not entry in entries_to_filter:
            copy_entries.append(entry)
    entries = copy_entries

    # Select randomly three enries to render.
    if len(entries) > 3:
         entries = random.sample(entries, 3)
    entries = sorted(entries, key=lambda expression: expression.id )
    return render_template('entries.html', entries=entries)

@app.route('/repeat', methods=['GET', 'POST'])
def repeat():
    username = request.cookies.get('username')
    entries = Expression.query.join(Favorites).filter_by(user_name=username).all()
    # Select randomly five enries to render.
    if len(entries) > 3:
         entries = random.sample(entries, 3)
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

@app.route('/addfavorite/<int:id>')
def addfavorite(id):
    username = request.cookies.get('username')
    if username:
        favorite = Favorites(username, id)
        db.session.add(favorite)
        db.session.commit()
    return "success" 

@app.route('/removefavorite/<int:id>')
def removefavorite(id):
    username = request.cookies.get('username')
    if username:
        favorite = Favorites.query.filter_by(user_name=username).filter_by(expression_id = id).first()
        db.session.delete(favorite)
        db.session.commit()
    return "success" 



