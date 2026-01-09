from flask import Flask, render_template, request

from pymongo import MongoClient



app = Flask(__name__)



# 1. MongoDB Connection Setup

try:

    # Adding a timeout so it doesn't hang if MongoDB is off

    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)

    db = client["student_db"]

    students_collection = db["students"]

    # Check connection

    client.server_info() 

    print(">>> Success: Connected to MongoDB!")

except Exception as e:

    print(f">>> ERROR: Could not connect to MongoDB: {e}")



@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':

        try:

            student_data = {

                "name": request.form.get("name"),

                "roll_number": request.form.get("roll_number"),

                "year": request.form.get("year"),

                "semester": request.form.get("semester"),

                "gender": request.form.get("gender"),

                "email": request.form.get("email"),

                "languages": request.form.getlist("languages"), 

                "address": request.form.get("address")

            }



            students_collection.insert_one(student_data)

            return "<h1>Success!</h1><p>Data Saved.</p><a href='/'>Go Back</a>"

        except Exception as e:

            return f"Error saving data: {e}"



    return render_template('index.html')



# IMPORTANT: Ensure these two lines are at the VERY BOTTOM 

# and have ZERO spaces before them.

if __name__ == '__main__':

    print(">>> Flask server is starting...")

    app.run(debug=True, port=5000)