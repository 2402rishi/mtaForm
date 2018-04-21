from flask import render_template, flash, redirect,request,url_for
from app import app
from flask_mail import Mail, Message
from flask_cors import CORS
from app import db
from app.models import User
from dateutil.parser import parse
from datetime import date
import datetime
from .decorators import async
from app import mail
@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)


def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False
def date_convert(value):
	if(is_date(value)):
		value= value.split("-")
		return datetime.date(int(value[0]),int(value[1]),int(value[2]))

CORS(app)


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/send',methods=['GET', 'POST'])
def your_view():
    if request.method == 'POST':
        print (request.form)
        print ("in here")
        if request.form['button_value'] == str("user"):
            print ("Hello User")
            u = User(coordinator = request.form["coordinator"], \
                 user_req = request.form["user_req"], \
                 site_code = request.form["site_code"], \
                 submit_date = date_convert(str(request.form["submit_date"])) , \
                 due_date = date_convert(str(request.form["due_date"])), \
                 install = True if "install" in request.form else False, \
                 change = True if "change" in request.form else False, \
                 move = True if "move" in request.form else False, \
                 disconnect = True if "diconnect" in request.form else False, \
                 requestor_name = request.form["requestor_name"], \
                 email = request.form["email"], \
                 telephone = request.form["telephone"], \
                 department = request.form["department"], \
                 division = request.form["division"], \
                 rc = request.form["rc"], \
                 address = request.form["address"], \
                 room = request.form["room"], \
                 depot = request.form["depot"], \
                 description = request.form["description"], \
                 manager_name = request.form["manager_name"], \
                 manager_title = request.form["manager_title"], \
                 approval = False, \
                 floor = request.form["floor"] \
                 )
            print (u)
            print (db.session.add(u))
            print (db.session.commit())
            print (u.key)
            link = "https://mta-it.herokuapp.com/"+"id/{}".format(u.key)
            send_email("Approval request","rishi.agarwal@nyct.com",["rda311@nyu.edu"],"Please aprrove the form \n {}".format(link),"")
            return redirect(url_for("index"),code=302)
        elif request.form['button_value'] == str("manager"):
            print("Manager")
            u = User.query.filter_by(key=int(str(request.form["key"]))).first()
            send_email("Approval request","rishi.agarwal@nyct.com",[u.email,"rishi.agarwal@nyct.com"],"your request has been approved","")
            u.approval=True
            db.session.commit()
            return redirect(url_for('reset'),code=302)
        else:
            return redirect("/")
    elif request.method == 'GET':
        return render_template('index.html')
    
@app.route('/reset',methods=["GET","POST"])
def reset():
	return render_template("approval.html")
@app.route("/try")
def new_one():
    # return render_template('index.html',user={"requestor_name":'Rishi Agarwal', "manager_name":"Jeff Skidmore","coordinator":1,"site_code":23,"uid":12,"submit_date":"02/23/1994","due_date":"02/23/1995","disconnect":1})
    return render_template("index.html",user=User.query.all()[-1])

@app.route('/id/<int:user_id>')
def manager_approval(user_id):
	u = User.query.filter_by(key=user_id).first()
	return render_template("index.html",user=u)

