from flask import Flask, render_template, redirect, request
from models import db, Student


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tiger@localhost/studentcrud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# @app.before_first_request
# def create_table():
#     db.create_all()
with app.app_context():
    db.create_all()

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    
    if request.method == "POST":
        # hobby = request.form.getlist('hobbies')
        # hobbies = ",".join(map(str, hobby))
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        hobbies = ', '.join(request.form.getlist('hobbies'))
        country = request.form.get('country')

        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')

@app.route('/', methods=["GET"])   
def RetriveList():
    students = Student.query.all()
    return render_template('index.html', students=students)



# @app.route('/<int:id>/edit', methods=["GET","POST"])
# def update(id):
#     student = Student.query.get_or_404(id)
#     if request.method == "POST":
#         db.session.delete(student)
#         db.session.commit()
#         if student:
#             first_name = request.form['first_name']
#             last_name = request.form['last_name']
#             email = request.form['email']
#             password = request.form['password']
#             gender = request.form['gender']
#             hobbies = ', '.join(request.form.getlist('hobbies'))
#             country = request.form['country']

#             student = Student(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 password=password,
#                 gender=gender,
#                 hobbies=hobbies,
#                 country=country
#             )

#             db.session.update(student)
#             db.session.commit()
#             return redirect('/')
#         return f"student with id = {id} Does not found"

#     return render_template("update.html", student=student)

@app.route('/<int:id>/edit', methods=["GET", "POST"])
def update(id):
    # This will automatically return 404 if student doesn't exist
    student = Student.query.get_or_404(id)
    
    if request.method == "POST":
        # Update existing student object
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.email = request.form['email']
        student.password = request.form['password']  # Should hash passwords!
        student.gender = request.form['gender']
        student.hobbies = ', '.join(request.form.getlist('hobbies'))
        student.country = request.form['country']

        db.session.commit()
        return redirect('/')
    
    return render_template("update.html", student=student)


@app.route("/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    student = Student.query.filter_by(id=id).first()
    if request.method == "POST":
        if student:
            db.session.delete(student), 404
            db.session.commit()
            return redirect('/')
        abort(404)
    else:
        return render_template('delete.html')

    


if __name__ == "__main__":
    app.run(debug=True)