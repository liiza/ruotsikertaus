from wtforms import Form, TextField, validators

class AddEntryForm(Form):
	finnish = TextField('Suomenkielinen ilmaisu', [validators.Length(min=10, max=200)])
	swedish = TextField('Ruotsinkielinen ilmaisu', [validators.Length(min=10, max=200)])
	
