from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/codingthunder'
db=SQLAlchemy(app)
   
class Mydata(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),nullable=False)
    password=db.Column(db.String(30),nullable=False)

class Length(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    questionlength=db.Column(db.String(30),nullable=False)
    optionlength=db.Column(db.String(30),nullable=False)

class Form(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(100),nullable=False)
    questiontable=db.relationship("Question",backref="form")
    table=db.relationship("Option",backref="form")
    

class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(100),nullable=False)
    form_id=db.Column(db.Integer,db.ForeignKey("form.id"))
    optiontable=db.relationship("Option",backref="question")
    

class Option(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    option=db.Column(db.String(100),nullable=False)
    question_id=db.Column(db.Integer,db.ForeignKey("question.id"))
    form_id=db.Column(db.Integer,db.ForeignKey("form.id"))

class Response(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    option=db.Column(db.String(100),nullable=False)
    question_id=db.Column(db.Integer)
    form_id=db.Column(db.Integer)

@app.route("/")
def index():
    
    return render_template("login.html")
    

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        
        if password==confirm:
                entry=Mydata(email=email,password=password)
                db.session.add(entry)
                db.session.commit()
                return render_template("login.html")
        else:
            return render_template("signup.html")
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email = str(request.form['email'])
        password = str(request.form['password'])
        missing = Mydata.query.filter_by(email=email).first()
        if missing is None:
            return render_template("login.html")
        else:
            if missing.password==password:
                return render_template("length.html")
        return render_template("login.html")
    
@app.route("/form",methods=["GET","POST"])
def form():
    
    if request.method=="POST":
        title1=request.form.get("title")
        description1=request.form.get("description")
        form1=Form(title=title1,description=description1)
        db.session.add(form1)
        questionarray=request.form.getlist("question")
        optionarray=request.form.getlist("option")
        data=Length.query.all()
        length=Length.query.filter_by(id=data[-1].id).first()
        p=length.questionlength
        q=length.optionlength
        k=0
        for i in range(0,p):
            ent=Question(question=questionarray[i],form=form1)
            db.session.add(ent)
            for j in range(0,q):
                entr=Option(option=optionarray[k],question=ent,form=form1)
                db.session.add(entr)
                k+=1
        db.session.commit()
        obj=Form.query.all()
        page=Form.query.filter_by(id=obj[-1].id).first()
        quests=Question.query.filter_by(form_id=obj[-1].id).all()
        quest=Question.query.filter_by(form_id=obj[-1].id).first()
        return render_template("page.html",page=page,quest=quest,quests=quests,value=q)
    return render_template("form.html")

                             
@app.route("/page",methods=["GET","POST"])
def page():
    if request.method=="POST":
        obj=Form.query.all()
        page=Form.query.filter_by(id=obj[-1].id).first()
        questions=Question.query.filter_by(form_id=obj[-1].id).all()
        question=Question.query.filter_by(form_id=obj[-1].id).first()
        for question in questions:
            p=str(question.id)
            rightoption=request.form.get(p)
            entry=Response(option=rightoption,question_id=question.id,form_id=page.id)
            db.session.add(entry)
            db.session.commit()
        return render_template("submit.html")
    return render_template("submit.html")


@app.route("/response")
def response():
    obj=Form.query.all()
    page=Form.query.filter_by(id=obj[-1].id).first()
    quests=Question.query.filter_by(form_id=obj[-1].id).all()
    quest=Question.query.filter_by(form_id=obj[-1].id).first()
    rightoptions=Response.query.filter_by(form_id=obj[-1].id).all()
    rightoption=Response.query.filter_by(form_id=obj[-1].id).first()
    return render_template("response.html",page=page,quest=quest,quests=quests,rightoptions=rightoptions,rightoption=rightoption)

@app.route("/length",methods=["GET","POST"])
def length():
    if request.method=="POST":
        question=request.form.get("questionlength")
        option=request.form.get("optionlength")
        entry=Length(questionlength=question,optionlength=option)
        db.session.add(entry)
        db.session.commit()
        return render_template("form.html")
    return render_template("length.html")

if __name__ == '__main__':
   app.run(debug=True)
