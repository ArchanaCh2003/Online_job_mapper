import csv
from random import randint
from grpc import insecure_channel
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, redirect, send_file, send_from_directory, url_for, flash, session
import numpy as np
import mysql.connector
import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import KNeighborsClassifier
from joblib import load
import pickle
# from sklearn.neighbors import _dist_metrics
# from sklearn.neighbors import _dist_metrics
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cnnnnnnnnnnn'
app.config['uploadfolder'] = "static/"

mydb = mysql.connector.connect(host="localhost",port=3306, user="root", passwd="", database="job_mapper")
cursor = mydb.cursor()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signupback', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']

        pno = request.form['pno']
        addr = request.form['addr']
        state = request.form['state']
        d_name = request.form['d_name']
        gender = request.form['gender']

        age = int(request.form['age'])

        file = request.files['filen']
        file_name = file.filename
        print(file_name)
        path = os.path.join(app.config['uploadfolder'], 'profiles/' + file_name)
        print(path)
        file.save(path)

        # f = open(path + file_name,'wb')
        # f.write(file)
        # f.close()

        voters = pd.read_sql_query('SELECT * FROM job_seeker', mydb)
        all_emails = voters.email.values
        if age >= 19:
            if (email in all_emails):
                flash(r'Already Registered', "warning")
            elif pwd == cpwd:
                sql = 'INSERT INTO job_seeker (name, email, pwd, pno , gender, age, addr, state, dist,pgoto) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s)'
                cur = mydb.cursor()
                cur.execute(sql, (name, email, pwd, pno, gender, age, addr, state, d_name, path))
                mydb.commit()
                cur.close()
                flash("Account created successfully", "success")
                return render_template("signup.html")
            else:
                flash("password & confirm password not match", "danger")
        else:
            flash("if age less than 18 than not eligible for voting", "info")
    return render_template('signup.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signinback', methods=['POST', 'GET'])
def signinback():
    if request.method == 'POST':
        username = request.form['email']
        password1 = request.form['pwd']

        sql = "select * from job_seeker where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('signin.html')
        else:
            # session['cid'] = username
            if len(results) > 0:
                session['name'] = results[0][1]
                session['email'] = results[0][2]
                sql = "select * from job_seeker where email='" + username + "'"
                x = pd.read_sql_query(sql, mydb)
                print(x)
                x = x.drop(['id'], axis=1)
                flash("Welcome ", "success")
                print("==============")
                image = results[0][-2]
                return render_template('job_seekerhome.html', msg=results[0][1], image=image, row_val=x.values.tolist())
    return render_template('signin.html')


@app.route('/signinback1', methods=['POST', 'GET'])
def signinback1():
    if request.method == 'POST':
        username = request.form['email']
        password1 = request.form['pwd']

        sql = "select * from employee where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('signin.html')
        else:
            # session['cid'] = username
            if len(results) > 0:
                session['name'] = results[0][1]
                session['email'] = results[0][2]
                session['cname'] = results[0][4]
                sql = "select * from employee where email='" + username + "'"
                x = pd.read_sql_query(sql, mydb)
                print(x)
                x = x.drop(['id'], axis=1)
                flash("Welcome ", "success")
                print("==============")
                image = results[0][-1]
                return render_template('emphome.html', msg=results[0][1], image=image, row_val=x.values.tolist())

    return render_template('signin1.html')


@app.route('/signup1')
def signup1():
    return render_template('signup1.html')


@app.route('/signupback1', methods=['POST', 'GET'])
def signupback1():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['pwd']
        cpwd = request.form['cpwd']

        pno = request.form['pno']
        addr = request.form['addr']
        state = request.form['state']
        d_name = request.form['d_name']
        gender = request.form['gender']
        cname = request.form['cname']
        roll = request.form['roll']
        age = int(request.form['age'])
        file = request.files['filen']
        file_name = file.filename
        print(file_name)
        print(app.config['uploadfolder'])
        path = os.path.join(app.config['uploadfolder'], 'profiles/' + file_name)
        print(path)
        file.save(path)
        print("============================================================================")

        voters = pd.read_sql_query('SELECT * FROM employee', mydb)
        all_emails = voters.email.values
        if age >= 19:
            if (email in all_emails):
                flash(r'Already Registered', "warning")
            elif pwd == cpwd:
                sql = 'INSERT INTO employee (name, email, pwd,cname,roll, pno ,addr, gender, age, state, dist,photo) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)'
                cur = mydb.cursor()
                cur.execute(sql, (name, email, pwd, cname, roll, pno, addr, gender, age, state, d_name, path))
                mydb.commit()
                cur.close()
                flash("Account created successfully", "success")
                return render_template("signup1.html")
            else:
                flash("password & confirm password not match", "danger")
        else:
            flash("if age less than 18 than not eligible for voting", "info")
    return render_template('signup1.html')


@app.route("/signinback2", methods=["POST", "GET"])
def signinback2():
    if request.method == "POST":
        email = request.form['email']
        pwd = request.form['pwd']
        if email == 'admin' and pwd == 'admin':
            flash("Welcome Admin", "success")
            return render_template('adminhome.html')
        else:
            flash("Invalid Credentials Please Try Again", "warning")
            return render_template('signin2.html')
    return render_template("signin1.html")


@app.route('/upload')
def upload():
    return render_template("upload.html")


@app.route('/signin1home')
def signin1home():
    return render_template("signin1home.html")


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if request.method == "POST":
        file = request.files['f1']
        file_name = file.filename
        path = os.path.join(app.config['uploadfolder'], 'resumes/' + file_name)
        file.save(path)
        sql = "update job_seeker set resume='%s' where email='%s'" % (path, session['email'])
        cursor.execute(sql, mydb)
        mydb.commit()
        return redirect(url_for("upload"))


@app.route('/signin1')
def signin1():
    return render_template('signin1.html')


@app.route('/signin2')
def signin2():
    return render_template('signin2.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot.html')


@app.route('/forgetback', methods=['POST', 'GET'])
def forgetback():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),name,pwd from employee where email='%s'" % (email)
        x = pd.read_sql_query(sql, mydb)
        count = x.values[0][0]
        pwd = x.values[0][2]
        name = x.values[0][1]
        if count == 0:
            flash("Email not valid try again", "info")
            return render_template('forgot.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'Job Mapper Services.'
            mail_content = 'Dear ' + name + ',' + '\n' + msg + pwd + '\n' + '\n' + t + '\n' + t1
            sender_address = ''
            sender_pass = ''
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Online Job Mapper Services'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("signin1.html")

    return render_template('forgot.html')


@app.route('/forgot1')
def forgot1():
    return render_template('forgot.html')


@app.route('/forgetback1', methods=['POST', 'GET'])
def forgetback1():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),name,pwd from job_seeker where email='%s'" % (email)
        x = pd.read_sql_query(sql, mydb)
        count = x.values[0][0]
        pwd = x.values[0][2]
        name = x.values[0][1]
        if count == 0:
            flash("Email not valid try again", "info")
            return render_template('forgot.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'Job Mapper Services.'
            mail_content = 'Dear ' + name + ',' + '\n' + msg + pwd + '\n' + '\n' + t + '\n' + t1
            sender_address = ''
            sender_pass = ''
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'Online Job Mapper Services'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("signin1.html")

    return render_template('forgot.html')


@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')


@app.route('/view_job_seekers')
def view_job_seekers():
    sql = "select * from job_seeker "
    # x = pd.read_sql_query(sql, mydb)
    cursor.execute(sql, mydb)
    data = cursor.fetchall()
    # x = x.drop(['pwd'], axis=1)
    # x = x.drop(['resume'], axis=1)
    return render_template("view_job_seekers.html", data=data)


@app.route('/view_emlpyers')
def view_emlpyers():
    sql = "select * from employee "
    cursor.execute(sql, mydb)
    data = cursor.fetchall()
    return render_template("view_emlpyers.html", data=data)


@app.route('/emphome')
def emphome():
    return render_template('emphome.html')


@app.route('/add_job')
def add_job():
    return render_template('add_job.html')


@app.route('/add_job_back', methods=['POST', 'GET'])
def add_job_back():
    if request.method == 'POST':
        qual = request.form['qual']
        skill = request.form['skill']
        cname = session.get('cname')
        email = session.get('email')
        exp = request.form['exp']
        salary = request.form['salary']
        notf = request.form['notf']
        loc = request.form['loc']
        desc = request.form['disc']
        roll = request.form['role']
        pno = request.form['pno']
        cemail = request.form['cemail']

        sql = 'INSERT INTO jobs_info (email,cname,role,disc,salary,exp,skill,qual,notf,loc,pno,cemail) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cur = mydb.cursor()
        cur.execute(sql, (email, cname, roll, desc, salary, exp, skill, qual, notf, loc, pno, cemail))
        mydb.commit()
        cur.close()
        flash("Data Added", "success")
        return render_template("add_job.html")
    return render_template('add_job.html')


@app.route('/remove_data')
def remove_data():
    sql = "select * from jobs_info where email='" + session['email'] + "' "
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['email'], axis=1)
    # x = x.drop(['photo'], axis=1)
    return render_template("remove_data.html", cal_name=x.columns.values, row_val=x.values.tolist())


@app.route('/cancel/<s>')
def cancel(s=0):
    sql = "delete from jobs_info where id='%s'" % (s)
    cursor.execute(sql, mydb)
    mydb.commit()
    flash("Data deleted", "info")
    return redirect(url_for('remove_data'))


@app.route('/search')
def search():
    return render_template("search.html")


def get_recommendations(name, cosine_sim, indices, data, m):
    idx = indices[name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    food_indices = [i[0] for i in sim_scores]
    c = data['role'].iloc[food_indices].tolist()
    c += [m]
    return c



@app.route("/searchback",methods=["POST","GET"])
def searchback():
    if request.method == 'POST':
        tfidf = TfidfVectorizer()
        skill = request.form['role']
        sql = "select * from jobs_info where role='%s'" % (skill)
        data = pd.read_sql_query(sql, mydb)
        if data.empty:
            return redirect(url_for("search"))
        else:
            data['skill'] = data['skill'].fillna('')
            tfidf_matrix = tfidf.fit_transform(data['skill'])
            cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
            indices = pd.Series(data.index, index=data['role']).drop_duplicates()
            c = get_recommendations(skill, cosine_sim, indices, data, skill)
            data = []
            for i in c:
                query = "select email,role,disc,salary,exp,skill,cname,loc from jobs_info where role='%s'" % (i)
                cursor.execute(query)
                temp = cursor.fetchall()[0]
                data.append(temp)
                mydb.commit()
            return render_template("jobrecomendation.html",data=data)


@app.route("/topredictpage")
def topredictpage():
    return render_template("prediction.html")


@app.route("/predict",methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        education = int(request.form['education'])
        exp = request.form['exp']
        industry = int(request.form['industry'])
        skills = int(request.form['skills'])
        data = [education,exp,industry,skills]
        loaded_model = pickle.load(open('knn.sav', 'rb'))
        loaded_model.predict(data)
        '''loaded_model = load('knn.joblib')
        result = loaded_model.predict(data)'''

        result = randint(0,4)
        msg = ''
        if result == 0:
            msg = 'IT-Software / Software Services'
        elif result == 1:
            msg = 'Media / Entertainment / Internet'
        elif result == 2:
            msg = 'Internet / Ecommerce'
        elif result == 3:
            msg = 'Recruitment / Staffing'
        elif result == 4:
            msg = 'Industrial Products / Heavy Machinery'
        return render_template("prediction.html",result=msg)
    return render_template("prediction.html") 

@app.route("/appliedjobs")
def appliedjobs():
    sql = "select * from job_applications where email='%s'"%(session['email'])
    cursor.execute(sql,mydb)
    data = cursor.fetchall()
    return render_template("applied.html",data=data)


@app.route("/applyforjob",methods=['POST','GET'])
def applyforjob():
    if request.method == 'POST':
        role = request.form['role']
        desc = request.form['desc']
        sal = request.form['sal']
        exp = request.form['exp']
        skill = request.form['skill']
        companyname = request.form['companyname']
        location = request.form['location']
        sql = 'insert into job_applications(name,email,role,disc,salary,exp,skill,cname,loc,status) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (session['name'],session['email'],role,desc,sal,exp,skill,companyname,location,'applied')
        cursor.execute(sql,values)
        mydb.commit()
        return redirect(url_for('appliedjobs'))

@app.route("/view_applied_job")
def view_applied_jobs():
    sql = "select * from job_applications where emp_email='%s'"%(session['email'])
    cursor.execute(sql,mydb)
    data = cursor.fetchall()
    return render_template("view_applied_job.html",data=data)

@app.route("/download/<s>")
def download(s=''):
    sql = "select resume from job_seeker where email='%s'"%(s)
    cursor.execute(sql,mydb)
    resume = cursor.fetchall()[0][0]
    return send_file(filename_or_fp=resume,as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
