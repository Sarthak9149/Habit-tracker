from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

# command to run the file - flask --app app.py --debug run

# to get the current date time
def get_current_date():
    today = date.today()
    return today.strftime("%B %d, %Y")

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def index():
    return render_template("index.html", current_date = get_current_date())

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/success", methods=["GET", "POST"])
def success():
    required_fields = ['name', 'gender', 'dob', 'email', 'password', 'confirm_password']
    for field in required_fields:
        value = request.form.get(f"{field}")
        if not value:
            display_name = field.replace("_", " ").title()
            return render_template("error.html", message = f"Missing {display_name}")
        elif (request.form.get("password") != request.form.get("confirm_password")):
            return render_template("error.html", message="Enter same password")
        
    
    try:
        with sqlite3.connect('users.db') as connection:
            cursor = connection.cursor()
            sql = """CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, 
            dob TEXT, email NOT NULL UNIQUE, PASSWORD NOT NULL)"""
            cursor.execute(sql)
            connection.commit()
            
            # inserting data into users database
            new_required_fields = ['name', 'gender', 'dob', 'email', 'password']
            values_to_insert = [request.form.get(field) for field in new_required_fields]
            

            cursor.execute("""INSERT INTO users (name, gender, DOB, email, password) VALUES (?, ?, ?, ?, ?)""", tuple(values_to_insert))
            connection.commit()

    except sqlite3.IntegrityError:
        return render_template("error.html", message="This email is already registered.")
    
    except sqlite3.Error as e:
        return render_template("error.html", message=f"Database Error: {e}")

    return render_template("success.html")


@app.route("/loginsuccessfull", methods=["POST"])
def login_completed():
    email = request.form.get("email")
    password = request.form.get("password")

    # Check credentials in the database
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        

        if user:
            return render_template("index.html", name=user[1], current_date = get_current_date())  # Example: Redirect to user dashboard
        else:
            return render_template("error.html", message="Invalid email or password.")



if __name__ == "__main__":
    app.run(debug=True)