import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'courserizer@gmail.com'

mail = Mail(app)

def get_content():
    if request.method == 'POST':
        url = request.form['url']
        print(url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

def send_email(name, email, message):
    try:
        msg = Message('Contact Form Submission', sender=os.getenv("MAIL_USERNAME"), recipients=[os.getenv("RECIPIENT_EMAIL")])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        return True
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        return False

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if send_email(name, email, message):
            flash("Your message has been sent successfully!")
        else:
            flash("There was an error sending your message. Please try again later.")

        return redirect(url_for('index'))
    return render_template("contactus.html")

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/use')
def how_to_use():
    return render_template('howtouse.html')

if __name__ == "__main__":
    app.run(debug=True)
