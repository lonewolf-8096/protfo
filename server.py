from flask import Flask, render_template
from flask import request, redirect
import csv
import pyodbc
import psycopg2

app = Flask(__name__)


# @app.route('/blog')
# def blog():
#     return 'blog'
@app.route('/')
def index():
         return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('db.txt',mode='a') as db:
        email=data['email']
        subject=data['subject']
        message=data['message']
        file = db.write(f'\n{email},{subject}, {message}')


def write_to_csv(data):
    with open('db.csv', newline="", mode='a') as db2:
        email=data['email']
        subject=data['subject']
        message=data['message']
        csv_writer = csv.writer(db2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])





def insert_data(data):
    connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=127.0.0.1.saikrishna8096.pythonanywhere.com;'
                      'Database=PORTFOLIO;'
                      'Trusted_Connection=yes;')
    try:
            SQLCommand= ("INSERT INTO project" "(email,subj,msg)"
                      "VALUES (?,?,?)")
            Values=[data['email'],data['subject'],data['message']]
            cursor = connection.cursor()
            cursor.execute(SQLCommand, Values)
            connection.commit()
    except:
            print('Something wrong, please check')

    finally:
            # Close the connection
            connection.close()




def insert_data_2(data):
    email = data['email']
    subject = data['subject']
    message = data['message']
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="password",
                                      host="127.0.0.1.saikrishna8096.pythonanywhere.com",
                                      port="5432",
                                      database="PORTFOLIO")
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("\nYou are connected to - ", record, "\n")
        # Execute the sql query
        cursor.execute('Select * from project')

        # Print the data
        for row in cursor:
            print(row)
        cursor.execute( "INSERT INTO project(email,subj,msg) VALUES(%s,%s,%s)",(email,subject,message))
        connection.commit()
    except:
        print('Something wrong, please check2')

    finally:
        connection.close()






@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data=request.form.to_dict ()
        write_to_file(data)
        write_to_csv(data)
        insert_data(data)
        insert_data_2(data)
        #print(data)
        return redirect('/thankyou.html')
    else:
        return 'something went wrong'




#@app.route('/')
# def index():
#         return render_template('index.html')
#
#
# @app.route('/about.html')
# def about():
#     return render_template('about.html')
# @app.route('/works.html')
# def works():
#         return render_template('works.html')
#
# @app.route('/contact.html')
# def contact():
#     return render_template('contact.html')
#
#




