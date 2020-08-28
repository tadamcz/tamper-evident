from flask import Flask, render_template
from wtforms import TextAreaField, StringField, validators, BooleanField
import secrets
import hash
import json

from flask_wtf import Form, CSRFProtect #Flask-WTF provides your Flask application integration with WTForms.

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = secrets.csrf

class MyForm(Form):
    plaintext = TextAreaField('Enter message', [validators.Length(max=25)])
    whether_to_hash_message = BooleanField('Use hash of message?')
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
    form_data = form.data
    header_chain = hash.append_header(
        string_to_add=form_data['plaintext'],
        username=form_data['twitter_username'],
        do_hashing=form_data['whether_to_hash_message'])

    header_chain_pretty_json = json.dumps(header_chain,indent=4)
    return render_template('result.html', results=header_chain_pretty_json)

@csrf.exempt #I believe we don't need CSRF for a site without any user accounts
@app.route('/checkchain',methods=['GET'])
def check_chain():
    results = hash.check_integrity_of_chain()
    return render_template('result.html', results=results)

if __name__ == "__main__":
	app.run(debug=True)

