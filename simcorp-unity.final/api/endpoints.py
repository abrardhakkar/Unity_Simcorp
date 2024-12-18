from datetime import date
from functools import wraps
from flask import Blueprint, Flask, Response, current_app, jsonify, render_template, request, redirect, send_file, session, url_for
from passlib.hash import sha256_crypt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
from flask_mysqldb import MySQL

endpoints = Blueprint('endpoints', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@endpoints.record_once
def configure_mysql(state):
    mysql.init_app(state.app)
    state.app.config['MYSQL_HOST'] = 'localhost'
    state.app.config['MYSQL_USER'] = 'root'
    state.app.config['MYSQL_PASSWORD'] = 'Juve-2219'
    state.app.config['MYSQL_DB'] = 'family_office'
    state.app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configure MySQL connection
mysql = MySQL()


@endpoints.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']

        # Form validation
        if not username or not password:
            error = 'Please fill in all the fields'
            return render_template('login.html', error=error)

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Retrieve the user from the database
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            user = cur.fetchone()
            db_password = user['password']

            # Verify the password
            if sha256_crypt.verify(password, db_password):
                # Store user details in the session
                session['logged_in'] = True
                session['username'] = username

                # Redirect to the home page
                return redirect('/api/dashboard')
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

@endpoints.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fullname = request.form['fullname']

           # Form validation
        if not username or not password or not email or not fullname:
            error = 'Please fill in all the fields'
            return render_template('register.html', error=error)

        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Check if the username already exists
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            error = 'Username already exists'
            return render_template('register.html', error=error)

        # Hash the password
        hashed_password = sha256_crypt.hash(password)

        # Insert the new user into the database
        cur.execute("INSERT INTO users (username, password, email, fullname) VALUES (%s, %s, %s, %s)",
                    (username, hashed_password, email, fullname))
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the login page
        return redirect('/api')

    return render_template('register.html')

@endpoints.route('/dashboard')
@login_required
def home():
    # Check if the user is logged in
    if 'logged_in' in session:
        username = session['username']
        return render_template('dashboard.html', user={'username': username})

    # Redirect to the login page if not logged in
    return redirect(url_for('endpoints.login'))

@endpoints.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('endpoints.login'))

@endpoints.route('/stock', methods=['GET', 'POST'])
@login_required
def stock_form():
    if request.method == 'POST':
        # Retrieve form data
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Fetch stock data for the specified symbol and dates
        data = yf.download(symbol, start=start_date, end=end_date)

        # Convert the DataFrame to a list of dictionaries
        stock_data = data.reset_index().to_dict('records')

        # Pass the stock data and date range to the template
        return render_template('stock.html', symbol=symbol, stock_data=stock_data, start_date=start_date, end_date=end_date)

    return render_template('stock_form.html')

@endpoints.route('/stock/json', methods=['GET', 'POST'])
@login_required
def stock_json():
    if request.method == 'POST':
        # Retrieve form data
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Fetch stock data for the specified symbol and dates
        data = yf.download(symbol, start=start_date, end=end_date)

        # Convert the DataFrame to a list of dictionaries
        stock_data = data.reset_index().to_dict('records')

        # Return the stock data as a JSON response
        return jsonify(stock_data)

    return render_template('stock_form.html')

@endpoints.route('/plot/<symbol>/<start_date>/<end_date>')
def plot(symbol, start_date, end_date):
    # Retrieve stock data for the specified symbol and dates
    data = yf.download(symbol, start=start_date, end=end_date)

    # Generate the graph
    plt.figure(figsize=(12, 6))
    data['Close'].plot()
    plt.title(f'{symbol} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)

    # Save the graph to a BytesIO object
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Return the graph as an image
    return send_file(img_bytes, mimetype='image/png')

@endpoints.route('/save', methods=['POST'])
@login_required
def save_trade():
    if request.method == 'POST':
        # Retrieve form data
        company_name = request.form['company_name']
        trade = request.form['trade']
        amount = request.form['amount']

        trade_date = date.today().strftime("%Y-%m-%d")
        
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Insert the trade data into the table
        cur.execute("INSERT INTO trade (company_name, trade, amount, trade_date) VALUES (%s, %s, %s, %s)",
                    (company_name, trade, amount, trade_date))
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the trade page or any other desired location
        return redirect('/api/trade')

    # Handle other HTTP methods if necessary
    return redirect('/api/trade')

from flask import request


@endpoints.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    if request.method == 'POST':
        # Retrieve the trade ID from the form
        trade_id = request.form['trade_id']
        
        # Create a cursor to interact with the database
        cur = mysql.connection.cursor()

        # Delete the trade data from the table based on the trade ID
        cur.execute("DELETE FROM trade WHERE id = %s", [trade_id])
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Redirect to the portfolio page to show the updated data
        return redirect(url_for('endpoints.portfolio'))

    # Create a cursor to interact with the database
    cur = mysql.connection.cursor()

    # Fetch the trade data from the table
    cur.execute("SELECT * FROM trade")
    trade_data = cur.fetchall()

    # Close the cursor
    cur.close()

    # Render the HTML template and pass the trade data to it
    return render_template('portfolio.html', trade_data=trade_data)


@endpoints.route('/analyze')
@login_required
def analyze():
    # Add your stock page logic here
    return render_template('analyze.html')

@endpoints.route('/trade')
@login_required
def trade():
    # Add your trade page logic here
    return render_template('trade.html')

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = '002219'
app.register_blueprint(endpoints, url_prefix='/api')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
