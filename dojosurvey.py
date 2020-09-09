from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' 

@app.route('/')
def takeinfo():
    return render_template("dojosurvey.html")

@app.route('/route')
def getadd():
    mysql = connectToMySQL("dojosurvey")
    surveys = mysql.query_db("SELECT * FROM surveys;")
    return render_template("dojosurvey.html", name=name, dojo_location=dojo_location, favorite_language=favorite_language, comments=comments)

@app.route('/route', methods=['POST'])
def sqladd():
    is_valid = True
    if len(request.form['name'])<1:
        is_valid = False
        flash("Please enter name")
    if not is_valid: 
        return redirect('/')
    else:
        mysql = connectToMySQL("dojosurvey")
        query = "INSERT INTO surveys(name, dojo_location, favorite_language, comment, created_at, updated_at) VALUES (%(name)s, %(dojo_location)s, %(favorite_language)s, %(comment)s NOW(), NOW());"
        data = {
            "name": request.form["name"],
            "dojo_location": request.form["dojo_location"],
            "favorite_language": request.form["favorite_language"],
            "comments": request.form["comments"],
        }
        session["name"]=request.form["name"],
        session["dojo_location"]=request.form["dojo_location"]
        session["favorite_language"]=request.form["favorite_language"]
        session["comments"]=request.form["comments"]
        new_survey_id = mysql.query_db(query, data)
        flash("Friend successfully added!")
        return redirect("/submittedinfo")

@app.route('/submittedinfo')
def submittedinfo():
    name= session["name"],
    dojo_location=session["dojo_location"],
    favorite_language=session["favorite_language"],
    comments=session["comments"],
    return render_template("submittedinfo.html", name=name, dojo_location=dojo_location, favorite_language=favorite_language, comments=comments)
    
if __name__ == "__main__":
    app.run(debug=True)