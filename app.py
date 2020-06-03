from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/employees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class employees(db.Model):

    name = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.Integer())

    def __init__(self, name, designation, address, phone):
        self.name = name
        self.designation = designation
        self.address = address
        self.phone = phone


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    all_data = employees.query.all()

    return render_template("Index.html", employees=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        address = request.form['address']
        phone = request.form['phone']

        my_data = employees(name, designation, address, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = employees.query.get(request.form.get('name'))

        my_data.name = request.form['name']
        my_data.designation = request.form['designation']
        my_data.address = request.form['address']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<my_data>', methods=['GET', 'POST'])
def delete(my_data):
    my_data = employees.query.get('name')

    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)