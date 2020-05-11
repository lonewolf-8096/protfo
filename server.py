from flask import Flask, render_template
from flask import request, redirect
import csv
import pyodbc
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
                      'Server=LAPTOP-1UMNN0C2\SQLEXPRESS;'
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






@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data=request.form.to_dict ()
        write_to_file(data)
        write_to_csv(data)
        insert_data(data)
        print(data)
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




