import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, send_file, jsonify, Response
from main import CourseScraper
from flask_cors import CORS
from flask_mail import Mail, Message

from modules.chatbot import ChatBot 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")


CORS(app)
mail = Mail(app)
bot = ChatBot()


def send_email(name, email, message):
    try:
        msg = Message('Contact Form Submission',
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[os.getenv("RECIPIENT_EMAIL")])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        flash(f"An error occurred while sending email: {e}", 'error')
        return False

@app.route("/Korsy", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "No question provided."}), 400

    question = data["question"]

    def generate():
        for chunk in bot.stream_answer(question):
            yield chunk

    return Response(generate(), mimetype="text/plain")


@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request data."}), 400

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if send_email(name, email, message):
        return jsonify({"message": "Your message has been sent successfully!"}), 200
    else:
        return jsonify({"message": "There was an error sending your message. Please try again later."}), 500


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
        course_scraper = CourseScraper(url)
        course_scraper.scrape_course_info()
        file_path = course_scraper.file_path
        new_file_path = os.path.splitext(file_path)[0] + '.txt'
        os.rename(file_path, new_file_path)

        return render_template('result.html', file_path=new_file_path)
    else:
        return render_template('app.html')

# @app.route('/download', methods=['POST'])
# def download():
#     file_path = request.form.get('file_path')
#     file_name = request.form.get('file_name')
    
#     if file_path:
#         if file_name:
#             download_name = f'{file_name}.txt'
#         else:
#             download_name = 'downloaded_file.txt'
#         return send_file(file_path, as_attachment=True, mimetype='text/plain', download_name=f'{download_name}')
#     else:
#         return "File path not provided."

if __name__ == "__main__":
    app.run(debug=True)