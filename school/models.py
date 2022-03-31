from school import app, mysql,cursor


teacher='''create table Teacher(id int primary key not null auto_increment, name varchar(50),qualification varchar(50),experience varchar(50), subject varchar(50));'''
notices='''create table Notification(id int primary key not null auto_increment, title varchar(200), pic_name varchar(250), pic_data longblob);'''
parents='''create table Parent(id int primary key not null auto_increment, father varchar(50), mother varchar(50), phone int, email varchar(50));'''
classes='''create table Class(id int primary key, name varchar(100));'''
students='''create table Student(id int primary key not null auto_increment, name varchar(50), roll int, dob date, class_id int, foreign key(class_id) references Class (id), parent_id int, foreign key(parent_id) references Parent (id));'''
fees='''create table Fees(id int primary key, amount int, month varchar(20), student_id int, foreign key(student_id) references Student (id));'''
reg='''create table Register(id int primary key not null auto_increment, student_name varchar(50), father varchar(50), mother varchar(50), email varchar(50), gender varchar(10), phone int, address varchar(200), class int, dob date, pre_school varchar(200));'''
queries='''create table Query(id int primary key not null auto_increment, name varchar(100), email varchar(100), date date, phone int, message varchar(500));'''
admin='''create table Admin(id int primary key not null auto_increment, email varchar(50), password varchar(200));'''
result='''create table Result(id int primary key not null auto_increment, pdf_name varchar(200), pdf_data blob, class_id int, foreign key(class_id) references Class (id));'''
images = '''create table Image(id int primary key not null auto_increment, pic_name varchar(250), pic_data blob);'''

# cursor.execute(gallery)
# cursor.execute(notices)
# cursor.execute(parents)
# cursor.execute(classes)
# cursor.execute(students)
# cursor.execute(fees)
# cursor.execute(reg)
# cursor.execute(result)

