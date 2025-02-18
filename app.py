from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import os
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add a secret key to use session

def get_top_output():
    """Fetch the top command output"""
    try:
        result = subprocess.run(["top", "-b", "-n", "1"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching top output: {str(e)}"

@app.route('/')
def index():
    return "Welcome! Visit /htop to see system information."

@app.route('/htop', methods=["GET", "POST"])
def htop():
    # Check if the form is submitted
    if request.method == "POST":
        # Get the name entered by the user in the form
        name = request.form.get("name", None)
        if not name:
            return redirect(url_for('htop'))  # Redirect back if no name is entered

        session['name'] = name  # Store the name in session

    # Fetch name from session
    name = session.get('name', None)

    if not name:
        return render_template("ask_details.html")

    # Get the system username using the environment variable (dynamic for each user)
    username = os.environ.get("USER", "unknown")
    
    # Get the server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")
    
    # Fetch the top command output
    top_output = get_top_output()

    return render_template("htop.html", name=name, username=username, server_time=server_time, top_output=top_output)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
