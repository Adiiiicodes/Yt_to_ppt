from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os

# Import the functions from their individual files
from process_transcription import process_transcription
from generate_ppt_payload import generate_ppt_payload
from call_ppt_maker_api import call_pptmaker_api

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Necessary for session storage

# ------------------ Routes ------------------

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Get Started Page: User enters the YouTube link
@app.route('/get-started', methods=['GET', 'POST'])
def get_started():
    if request.method == 'POST':
        youtube_link = request.form.get('youtube_link')
        transcription = process_transcription(youtube_link)
        # Store transcription in session for later use in PPT generation
        session['transcription'] = transcription
        return redirect(url_for('show_transcription'))
    return render_template('get_started.html')

# Transcription Display Page with a button to generate PPT
@app.route('/transcription')
def show_transcription():
    transcription = session.get('transcription', '')
    # Simple HTML display with a link to generate the PPT
    html_content = f"""
    <h2>Transcription:</h2>
    <pre>{transcription}</pre>
    <br>
    <a href="{url_for('generate_ppt')}"><button>Generate PowerPoint Presentation</button></a>
    """
    return html_content

# Generate PPT from transcription
@app.route('/generate-ppt')
def generate_ppt():
    transcription = session.get("transcription")
    if not transcription:
        return "No transcription found. Please start over."
    # Convert transcription to PPTMaker API payload using the Groq API
    payload = generate_ppt_payload(transcription)
    ppt_file = call_pptmaker_api(payload)
    if ppt_file:
        # Store the generated file name in session (if needed)
        session['ppt_file'] = ppt_file
        return redirect(url_for("download_ppt"))
    else:
        return "Error generating PPT. Please try again."

# Endpoint to download the generated PPT file
@app.route('/download-ppt')
def download_ppt():
    ppt_file = session.get('ppt_file')
    if ppt_file and os.path.exists(ppt_file):
        return send_file(ppt_file, as_attachment=True)
    else:
        return "PPT file not found. Please try generating the presentation again."

# Additional routes for guidelines and documentation (using your provided HTML templates)
@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)
