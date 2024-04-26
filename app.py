import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from main import CourseScraper
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'anurag1843panda@gmail.com'

mail = Mail(app)

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
        flash(f"An error occurred while sending email: {e}", 'error')  # Provide feedback to the user
        return False

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if send_email(name, email, message):
            flash("Your message has been sent successfully!", 'success')  # Provide feedback to the user
        else:
            flash("There was an error sending your message. Please try again later.", 'error')  # Provide feedback to the user

        return redirect(url_for('index'))
    return render_template("contactus.html")

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/use')
def how_to_use():
    return render_template('howtouse.html')

@app.route('/myapp', methods=['GET', 'POST'])
def myapp():
    if request.method == "POST":
        url = request.form.get('url')
        name = request.form.get('name')

        course_scraper = CourseScraper(url, name)
                
        course_scraper.scrape_course_info()

        file_path = course_scraper.file_path

        new_file_path = os.path.splitext(file_path)[0] + '.txt'
        os.rename(file_path, new_file_path)

        return render_template('result.html', file_path=new_file_path)
    else:
        return render_template('app.html')

@app.route('/download', methods=['POST'])
def download():
    file_path = request.form.get('file_path')
    file_name = request.form.get('file_name')
    
    if file_path:
        if file_name:
            download_name = f'{file_name}.txt'
        else:
            download_name = 'downloaded_file.txt'
        return send_file(file_path, as_attachment=True, mimetype='text/plain', download_name=f'{download_name}')
    else:
        return "File path not provided."

if __name__ == "__main__":
    app.run(debug=True)
