import logging
from flask import Flask, redirect
from api.endpoints import endpoints

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '002219'

@app.route('/')
def redirect_to_api():
    return redirect('/api/', code=302)

if __name__ == '__main__':
    app.register_blueprint(endpoints, url_prefix='/api')
    app.run(debug=True)