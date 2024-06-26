from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from utils import get_pw
from send_mail import send_mail

# Initialize web app
app = Flask(__name__)

# Variable to indicate whether we are in development (dev) or production mode
ENV = 'prod'

# Variables for database access config
db_user = 'postgres'
pw = get_pw('pw.txt')
host = 'localhost'
db_name = 'reviews'

# Setting up database configurations
if ENV == 'dev': # Development environment
    app.debug = True
    # Local database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{pw}@{host}/{db_name}'
else:  # Production environment
    app.debug = False
    # Heroku database
    app.config['SQLALCHEMY_DATABASE_URI'] = r"postgres://chwrnxjxpwcnlz:5c0dbe1b5eeec662dfe5fb8ff447f8e2312445235eecea1135e594e7bd2670f5@ec2-107-20-234-175.compute-1.amazonaws.com:5432/ddng0euhnqh7lm"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    """
    Feedback object will represent our 'feedback' table.
    """
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


# Our homepage (index page)
@app.route('/')
def index():
    return render_template('index.html')

# Page returned after user presses submit
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Getting form data
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']

        # Prompt message if customer or dealer fields are blank
        if customer == "" or dealer == "" or comments == "":
            return render_template('index.html', message='Please enter required fields')

        # Check if user already submitted feedback
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            # If user hasn't submitted feedback yet
            data = Feedback(customer, dealer, rating, comments)
            # Add to database
            db.session.add(data)
            db.session.commit()
            # Send email notification
            send_mail(customer, dealer, rating, comments)
            # Show rendered confirmation page
            return render_template('success.html')

        # If user already present in database show prompt
        return render_template('index.html', message='You have already submitted feedback')


# Run app if this is the main script
if __name__ == "__main__":
    app.debug = True
    app.run()