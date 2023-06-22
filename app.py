from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
import re
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['UPLOAD_PATH'] = "./uploads"
app.secret_key = 'your secret key'

server = 'mysqlserver-rv.database.windows.net'
username = 'azureuser'
password = 'Mavbgl@656'
database = 'demodb'
driver= '{ODBC Driver 18 for SQL Server}'
#Driver={ODBC Driver 18 for SQL Server};Server=tcp:mysqlserver-rv.database.windows.net,1433;Database=demodb;Uid=azureuser;Pwd={your_password_here};
conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password+ ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/selectBQuery', methods=['POST'])
def selectBQuery():
    time1 =request.form['time1']
    time2 =request.form['time2']

    # print("MAG1",type(mag1).__name__)
    # print("MAG2",type(mag1).__name__)
    # print(mag1,mag2)

    #cursor.execute('''SELECT time,latitude, longitude, mag, place FROM [dbo].[demo_data] where mag>='2' and mag <'5';''')
    query = "select latitude, longitude, place , time from tablename where time >= " + time1 + " and time < " + time2 +";"
    print(query)
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    result = cursor.fetchall()
    #print(result)
    time_taken = end_time-start_time
    #print(result)
    return render_template('query2.html', tableData=result , time_taken = time_taken , query = query)


@app.route('/selectBQuery2', methods=['POST'])
def selectBQuery2():
    time1 =request.form['time1']
    time2 =request.form['time2']

    # print("MAG1",type(mag1).__name__)
    # print("MAG2",type(mag1).__name__)
    # print(mag1,mag2)

    #cursor.execute('''SELECT time,latitude, longitude, mag, place FROM [dbo].[demo_data] where mag>='2' and mag <'5';''')
    query = "select latitude, longitude, place , time from tablename where time >= " + time1 + " and time < " + time2 +";"
    print(query)
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    result = cursor.fetchall()
    #print(result)
    time_taken = end_time-start_time
    #print(result)
    return render_template('query3.html', tableData=result , time_taken = time_taken , query = query)



# def latlong2():
#     if request.method == 'POST':
#         timee = request.form['time']
#         print(type(timee))
#         cursor.execute("Select time, latitude, longitude, mag,net, place from tableName where time="+timee) 
#         data = cursor.fetchall()
#         return render_template('latlong.html', latlong = data)

# @app.route('/minmax', methods=['GET', 'POST'])   
# def minmax():
#         if request.method == 'POST':
#             minlat = request.form['minlat']
#             minlong = request.form['minlong']
#             maxlat = request.form['maxlat']
#             maxlong = request.form['maxlong']
            
#             cursor.execute("Select time, latitude, longitude, mag,net, place from tableName where \
#                            (latitude>="+minlat +"or longitude>="+ minlong +") and (latitude<" + maxlat + " or longitude<"+maxlong+")") 
#             data = cursor.fetchall() 
#             return render_template('minmax.html', minmax = data)
#         return render_template('minmax.html')



# @app.route('/addrecord', methods=['GET', 'POST'])
# def addrecord():
#     msg=''
#     if request.method == 'POST':
#         time = request.form['name']
#         latitude = request.form['phone']
#         longitude = request.form['state']
#         mag = request.form['salary']
#         net = request.form['grade']
#         place = request.form['room']
        
#         if upload_status[0] == 'Success':
#             temp_filename = upload_status[1]
#             picture_url = 'https://cse6332sa.blob.core.windows.net/images/' + temp_filename
#         else:
#             msg = 'Failed to upload file!!'
#             return render_template('addrecord.html', msg=msg)
#         sql = ('''
#         SELECT * FROM people WHERE phone=?
#         ''')
#         cursor.execute(sql, (phone))
#         account = cursor.fetchone()
#         if account:
#             msg = 'Person already exists'
#         elif not name or not phone or not state or not salary or not grade or not room or not keywords:
#             msg = 'Please fill all details'
#         else:
#             cursor.execute('''INSERT INTO tablename (time	INT,
#     latitude 
#     , longitude ,
#     mag	,
#     net,
#     place) 
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
#                          , (time,
#     latitude 
#     , longitude ,
#     mag	,
#     net,
#     place))
#             cursor.commit()
#             msg = 'You have successfully added !'
#             return render_template('addrecord.html', msg=msg)
#     # elif request.method == 'POST':
#     #     msg = 'Please fill out the form !'
#     return render_template('addrecord.html', msg=msg)

# @app.route('/deleterecord/<id>', methods=['GET', 'POST'])
# def deleterecord(id):
#     msg=''
#     cursor.execute("DELETE FROM people where id={}".format(id))
#     cursor.commit()
#     msg = 'Record successfully deleted !'
#     return redirect('/')
    
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=6600, threaded=True,debug=True)



