from flask import Flask, render_template, request
from wtforms import TextAreaField, StringField, validators
import secrets

from flask_wtf import Form, CSRFProtect #Flask-WTF provides your Flask application integration with WTForms.

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = secrets.csrf

class MyForm(Form):
    plaintext = TextAreaField('Enter text', [validators.Length(max=25)])
    twitter_username = StringField('Twitter username to mention')

@csrf.exempt #I believe we don't need CSRF for a site without any user accounts
@app.route('/',methods=['GET'])
def show_form():
    form = MyForm()
    return render_template('index.html', form=form)

@csrf.exempt #I believe we don't need CSRF for a site without any user accounts
@app.route('/',methods=['POST'])
def f():
    form = MyForm()
    results = form.data
    return render_template('result.html', results=results)

if __name__ == "__main__":
	app.run(debug=True)
