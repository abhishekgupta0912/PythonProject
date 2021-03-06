import re

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

regemail = '^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$'
# rephone = '[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
rephone = '((\+*)((0[ -]+)*|(91 )*)(\d{12}+|\d{10}+))|\d{5}([- ]*)\d{6}'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/curd'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


def checkp(phone):
    data = Data.query.all()
    res = True
    for i in data:
        if i.phone == phone:
            res = False
            break
    return res


def checke(email):
    data = Data.query.all()
    res = True
    for i in data:
        if i.email == email:
            res = False
            break
    return res


def update_checke(id, email):
    res = True
    x = Data.query.all()
    for i in x:
        if id == i.id:
            if i.email != email:

                if not checke(email):
                    res = False
    return res


def update_checkp(id, phone):
    res = True
    if (len(phone) != 10):
        res = False
    x = Data.query.all()
    for i in x:
        if id == i.id:
            if phone != i.phone:
                if not checkp(phone):
                    res = False
    return res


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


@app.route('/')
def index():
    page_num = request.args.get('page_num', 1, type=int)
    all_data = Data.query.paginate(per_page=10, page=page_num, error_out=True)
    return render_template("index.html", contact=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        if (re.search(regemail, email)):
            if (checke(email)):
                if (len(phone) == 10 and checkp(phone)):
                    my_data = Data(name, email, phone)
                    db.session.add(my_data)
                    db.session.commit()
                    flash("Contact Created")
                else:
                    flash("Contact Not Added")
            else:
                flash("Email Already exist")
        else:
            flash("Enter a Correct Email")

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        x = request.form['email']
        y = request.form['phone']
        if (not update_checke(my_data.id, x)):
            flash("Can't Update Email Already Exist")
        else:
            my_data.email = request.form['email']

        if (not update_checkp(my_data.id, y)):
            flash("Can't Update Phone No.")
        else:
            my_data.phone = request.form['phone']
            db.session.commit()
            flash("Contact Updated Successfully")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Contact Deleted Successfully")

    return redirect(url_for('index'))


@app.route("/search")
def search():
    name_search = request.args.get('name')
    all_contacts = Data.query.filter(
        Data.name.contains(name_search)
    ).order_by(Data.name).all()
    return render_template('contact.html', contacts=all_contacts)


if __name__ == '__main__':
    app.run(debug=True)
