# task3
task



create a database name codingthunder
create following table
1.Mydata
  column=sno,email,password
2.Length
  column=questionlength,optionlength
3.Question
  column=id,question,form_id
4.Option
  column=id,option,question_id,form_id
5.Form
  column=id,title,description
6.Response
   column=id,option,question_id,form_id

uses XAMPP control and phpmyadmin....
open your control panel
1.pip install flask
2.pip install sqlalchemy
3.pip install virtualenv
4.set FLASK_APP=pro.py
5.flask run
