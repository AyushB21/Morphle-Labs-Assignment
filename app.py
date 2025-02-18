from flask import Flask, render_template
import subprocess
import os
from datetime import datetime
import pytz

app = Flask(__name__)

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

@app.route('/htop')
def htop():
    # Replace with your full name
    name = "Ayush Bhatt"
    # Get the system username using the environment variable
    username = os.environ.get("USER", "unknown")
    
    # Get the server time in IST
    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")
    
    # Fetch the top command output
    top_output = get_top_output()

    return render_template("htop.html", name=name, username=username, server_time=server_time, top_output=top_output)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
