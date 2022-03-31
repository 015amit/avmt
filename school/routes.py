from flask import Flask, render_template, request, jsonify, flash, session, send_file
from flask.helpers import url_for
from werkzeug.utils import redirect
from school import app,mysql
from io import BytesIO
import codecs
from datetime import datetime

@app.route('/')
def home():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select * from Notification;''')
    notices = cursor.fetchall()
    notices=list(notices)
    cursor.close()
    return render_template('home.html', title="Home", notices=notices)



@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'loggedin' in session:
        if session['username']=="admin":
            # return session['admin'];
            if request.method == 'POST':
                tname = request.form.get('tname')
                qualification = request.form.get('qualification')
                experience = request.form.get('experience')
                subject = request.form.get('subject')
                title = request.form.get('title')
                content = request.form.get('content')
                sname = request.form.get('sname')
                roll = request.form.get('roll')
                dob = request.form.get('dob')
                clas = request.form.get('class')
                father = request.form.get('father')
                mother = request.form.get('mother')
                phone = request.form.get('phone')
                email = request.form.get('email')
                img = request.files['timage']
                pdf = request.files['timage']
                
                if clas:
                    clas=int(clas)
                if title:
                    conn = mysql.connect()
                    cursor =conn.cursor()
                    cursor.execute('''insert into Notification(title, pic_name, pic_data) values (%s, %s, %s)''' , (title, title, pdf.read()))
                    conn.commit()
                    cursor.close()
                    flash(u'Notice is added','success')
                    return redirect(url_for('dashboard'))
                if tname:
                    conn = mysql.connect()
                    cursor =conn.cursor()
                    cursor.execute('''insert into Teacher(name, qualification, experience, subject, pic_name, pic_data) values (%s, %s, %s, %s, %s, %s)''' , (tname, qualification, experience, subject, "pic2", img.read()))
                    conn.commit()
                    cursor.close()
                    flash(f'Teacher is added','success')
                    return redirect(url_for('dashboard'))
                if sname:
                    father = str(father)
                    conn = mysql.connect()
                    cursor =conn.cursor()
                    
                    cursor.execute('''insert into Parent(father, mother, phone, email) values (%s, %s, %s, %s)''' , (father, mother, phone, email))
                    conn.commit()
                    cursor.execute('''select id from Parent where father = % s;''', (father))
                    pid = cursor.fetchone()
                    cursor.execute('''insert into Student(name, roll, dob, class_id, parent_id) values (%s, %s, %s, %s, %s)''' , (sname, roll, dob, clas, pid))
                    conn.commit()
                    cursor.close()
                    flash(f'Student is added','success')
                    return redirect(url_for('dashboard'))    
            return render_template('dashboard.html', title = 'Dashboard')
        return render_template("403.html")
    return redirect(url_for('login'))



@app.route('/dashboard/queries')
def queries():
    if session['username']=="admin":
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('''select * from Query;''')

        queries = cursor.fetchall()
        queries=list(queries)
        cursor.close()
        return render_template("query.html", queries=queries, title="Queries")
    return redirect(url_for('login'))



def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
    return binary_data


@app.route('/addimg', methods=['GET','POST'])
def addimg():
    img=request.form.get('img')
    img1= convert_data(img)
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''insert into Gallery(img) values (%s)''',(img1))
    conn.commit()
    cursor.close()
    return "hi hello"
    return jsonify(img)

@app.route('/dashboard/detail')
def detail():
    if session['username']=="admin":
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('''select * from Teacher;''')
        
        teachers = cursor.fetchall()
        cursor.execute('''select * from Notification;''')
        notices = cursor.fetchall()
        notices= list(notices)
        teachers=list(teachers)
        cursor.close()    

        return render_template('detail.html', teachers= teachers, title="Detail", notices=notices)
    return redirect(url_for('login'))

@app.route('/deletestudent/<int:id>', methods=['GET','POST'])
def deletestudent(id):
    if session['username']=="admin":
        if request.method=='POST':
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute('''DELETE FROM Student WHERE id = %d;'''%(int(id)))
            conn.commit()
            cursor.close()
            flash(f'Successfully deleted!','success')
            return redirect(url_for('studetails'))
    return redirect(url_for('login'))


@app.route('/deleteteacher/<int:id>', methods=['GET','POST'])
def deleteteacher(id):
    if session['username']=="admin":
        if request.method=='POST':
            conn = mysql.connect()
            cursor =conn.cursor()
            id=int(id)
            cursor.execute('''DELETE FROM Teacher WHERE id = %d;'''%(int(id)))
            conn.commit()
            cursor.close()
            flash(f'Successfully deleted!','success')
            return redirect(url_for('detail'))
    return redirect(url_for('login'))


@app.route('/deletenotice/<int:id>', methods=['GET','POST'])
def deletenotice(id):
    if session['username']=="admin":
        if request.method=='POST':
            conn = mysql.connect()
            cursor =conn.cursor()
            id=int(id)
            cursor.execute('''DELETE FROM Notification WHERE id = %d;'''%(int(id)))
            conn.commit()
            cursor.close()
            flash(f'Successfully deleted!','success')
            return redirect(url_for('detail'))
    return redirect(url_for('login'))





@app.route('/about')
def about():
    return render_template('about.html', title="AboutUs")



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Internal Server Error"), 500

@app.route('/faculty')
def faculty():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select * from Teacher;''')

    teachers = cursor.fetchall()
    teachers=list(teachers)
    
    cursor.close()
    return render_template('teacher.html', title="Teachers", teachers=teachers)


@app.route('/gallery')
def gallery():
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select id from Image order by id desc limit 1;''')
    last = cursor.fetchone()
    last = list(last)
    return render_template('gallery.html', title="Galleries", last=last)


@app.route('/co-curricular')
def curricular():
    return render_template("curricular.html", title="Co-Curricular")


@app.route('/rules')
def rule():
    return render_template("rule.html", title="School Rules")  


@app.route('/calendar')
def calendar():
    return render_template("calendar.html", title="Academic Calenadar")        

@app.route('/student_details')
def studetails():
    if session['username']=="admin":
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('''select * from Class;''')

        classes = cursor.fetchall()
        classes=list(classes)
        cursor.execute('''select * from Student;''')
        students = cursor.fetchall()
        students=list(students)
        cursor.execute('''select * from Parent;''')
        parents = cursor.fetchall()
        parents=list(parents)
        
        cursor.close()
        return render_template("studentdetails.html", classes=classes, students=zip(students,parents))
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET','POST'] )
def contact():
    if request.method == 'POST':
        name = request.form.get('uname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        mssg = request.form.get('mssg')
        date = datetime.now()
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('''insert into Query(name, email, date, phone, message) values (%s, %s, %s, %s, %s)''' , (name, email, date, phone, mssg))
        conn.commit()
        cursor.close()
    return render_template('contact.html', title="Contact Us")

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM Admin WHERE email = %s AND password = %s', (email, password,))
        account=cursor.fetchone()
        
        if account:
            
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['admin'] = True
            session['id'] = account[0]
            session['username']="admin"
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            flash(f'Incorrect email or password', "error")
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'] )
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        clss = request.form.get('class') 
        
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM Student WHERE roll = %s AND dob = %s AND class_id = %s', (name, dob, clss,))
        account=cursor.fetchone()
        
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['admin'] = False
            session['id'] = account[0]
            session['username']=account[1]
            # Redirect to home page
            return redirect(url_for('account'))
        else:
            # Account doesnt exist or username/password incorrect
            flash(f'Incorrect Credentials', "error")
            return "hi"
    return render_template('login.html', title="Student Login")


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('home'))


@app.route('/account')
def account():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('SELECT * FROM Student WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('student_info.html', title="Fees & Result", account=account)
    return redirect(url_for('login'))    

    



@app.route('/registration',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        fatname = request.form.get('fatname')
        motname = request.form.get('motname')
        email = request.form.get('email')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        clas = request.form.get('class')
        dob = request.form.get('dob')
        address = request.form.get('address')
        pschool = request.form.get('pschool')
        name = fname+lname
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute('''insert into Register(student_name, father, mother, email, gender, phone, class, dob, address, pre_school) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''' , (name, fatname, motname, email, gender, phone, clas, dob, address, pschool))
        conn.commit()
        cursor.close()
        return "student added"
    return render_template('registration.html', title="New Registration")

@app.route('/addimage', methods=['GET','POST'])
def addimage():
    if session['username']=="admin":
        if request.method == "POST":
            img = request.files['image']
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute('''insert into Image (pic_name, pic_data) values (%s, %s)''', ("pic2", img.read()))
            conn.commit()
            cursor.close()
            return "image uploaded"
    return page_not_found("error")


@app.route('/addresult', methods=['GET','POST'])
def addresult():
    if session['username']=="admin":
        if request.method == "POST":
            name = request.form.get('pdfname')
            pdfname = "class" + str(name)
            result = request.files['pdf']
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute('''insert into Result (id, pdf_name, pdf_data) values (%s, %s, %s)''', (name, pdfname, result.read()))
            conn.commit()
            cursor.close()
            return "Result uploaded"
    return page_not_found("error")


@app.route('/showresult/<int:id>')
def getresult(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select * from Result where id = %s''', (id))
    result = cursor.fetchone()
    result = list(result)
    result1 = result[2]
    # get = send_file(BytesIO(result[2]), attachment_filename='flask.pdf')
    cursor.close()
    header_byte = codecs.encode(result1[0:3], "hex")
    header_byte = str(header_byte).lower()
    header_byte = header_byte[2:8]

    if header_byte == '255044':
        get = send_file(BytesIO(result[2]), attachment_filename='flask.pdf')
    elif header_byte == '89504e':
        get = send_file(BytesIO(result[2]), attachment_filename='flask.png')
    elif header_byte == 'ffd8ff':
        get = send_file(BytesIO(result[2]), attachment_filename='flask.jpg')
    else:
        return "binary file"
    return get
    return get


@app.route('/show/<int:id>')
def getimg(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select * from Image where id = %s''', (id))
    image = cursor.fetchone()
    image = list(image)
    get = send_file(BytesIO(image[2]), attachment_filename='flask.png')
    cursor.close()
    return get


@app.route('/teacher/<int:id>')
def teacherimg(id):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select * from Teacher where id = %s''', (id))
    image = cursor.fetchone()
    image = list(image)
    get = send_file(BytesIO(image[6]), attachment_filename='flask.png')
    cursor.close()
    return get


@app.route('/notice/<string:title>.pdf')
def noticepdf(title):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute('''select * from Notification where title = %s''', (title))
    pdf = cursor.fetchone()
    pdf = list(pdf)
    get = send_file(BytesIO(pdf[3]), attachment_filename='notice.pdf')
    cursor.close()
    return get
