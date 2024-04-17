from flask import Flask, request, redirect, url_for, flash, session, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated user database
users_db = {}

# HTML template for login as a string
login_page_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Teacher Login Page</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .form-container {
            width: 300px;
            margin: 100px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 2px 2px 10px #ccc;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            display: inline-block;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            opacity: 0.8;
        }
        .errors {
            color: red;
            list-style-type: none;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form method="POST" action="/login">
            <h2>Login</h2>
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
            <p>Don't have an account? <a href="/register">Register here</a></p>
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    <ul class="errors">
                        {% for message in messages %}
                            <li>{{ message }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}
            {% endwith %}
        </form>
    </div>
</body>
</html>
"""

# HTML template for registration as a string
register_page_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Teacher Registration Page</title>
</head>
<body>
    <div class="form-container">
        <form method="POST" action="/register">
            <h2>Register</h2>
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
            <p>Already have an account? <a href="/login">Login here</a></p>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_db and users_db[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.')
    return render_template_string(login_page_html)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_db:
            flash('Username already exists.')
        else:
            users_db[username] = password
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
    return render_template_string(register_page_html)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome to your dashboard, {session['user']}!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
