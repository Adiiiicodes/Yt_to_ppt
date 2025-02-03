from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Get Started Page: User enters the YouTube link
@app.route('/get-started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        # Later: Add your transcription, Groq API, and PPTMaker API integration here.
        # For now, redirect to a dummy processing route.
        return redirect(url_for('process_link', youtube_link=youtube_link))
    return render_template('get_started.html')

# Dummy Processing Route (to be replaced with real processing logic)
@app.route('/process')
def process_link():
    youtube_link = request.args.get('youtube_link')
    # For now, simply display the link; later, process the link and generate a PPT.
    return f"<h2>Processing YouTube Link:</h2><p>{youtube_link}</p><p>(Backend processing will go here.)</p>"

# Guidelines Page
@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')

# Documentation Page
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)
