from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)

def get_content():
    if request.method == 'POST':
        url = request.form['url']
        print(url)

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

if __name__ == "__main__":
    app.run(debug=True)