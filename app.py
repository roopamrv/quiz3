from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
import re
import os
from werkzeug.utils import secure_filename
import time
import redis
import _pickle as cPickle
import random

app = Flask(__name__)
app.config['UPLOAD_PATH'] = "./uploads"
app.secret_key = 'your secret key'

red = redis.StrictRedis(host='roopamdns.redis.cache.windows.net',port=6380, db=0, password='UKpCfgBxKqwBwPo53Rjn7HNA7kl5JJaIjAzCaEuT3pg=', ssl=True)
#host=rds_hostname
result = red.ping()

server = 'mysqlserver-rv.database.windows.net'
username = 'azureuser'
password = 'Mavbgl@656'
database = 'demodb'
driver= '{ODBC Driver 18 for SQL Server}'
#Driver={ODBC Driver 18 for SQL Server};Server=tcp:mysqlserver-rv.database.windows.net,1433;Database=demodb;Uid=azureuser;Pwd={your_password_here};
conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password+ ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = conn.cursor()


print("Ping Returned : " + str(result))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query2', methods=['GET'])
def query2():
    return render_template('query2.html')

@app.route('/selectBQuery', methods=['POST'])
def selectBQuery():
    time1 =request.form['time1']
    time2 =request.form['time2']

    query = 'select latitude, longitude, place ,time from tableName where time >= '+ time1 + ' and time < ' + time2
    print("SQL1: " , query)
    start_time = time.time()
    cursor.execute(query)
    end_time = time.time()
    result = cursor.fetchall()
    #print(result)
    time_taken = end_time-start_time
    #print(result)
    
    start_time = time.time()
    #result = red.get('selectBQuery'+mag1+mag2)
    if red.get('selectBQuery'+time1+time2):
        result = cPickle.loads(red.get('selectBQuery'+time1+time2))
        end_time = time.time()
        time_taken = end_time-start_time
        print("returned from cache....", result)
    #cursor.execute('''SELECT time,latitude, longitude, mag, place FROM [dbo].[demo_data] where mag>='2' and mag <'5';''')
    else:
        start_time = time.time()
        cursor.execute(query)
        end_time = time.time()
        result = cursor.fetchall()
        time_taken = end_time-start_time
        print("Inside....")
        red.set('selectBQuery'+time1+time2,cPickle.dumps(result))

    return render_template('query2.html', tableData=result , time_taken = time_taken , query = query)

@app.route('/searchByLatAgeRandom', methods=['POST'])
def selectCQuery():
    print(request.form.get('count'))
    cursor = conn.cursor()
    #cursor.execute('select count(*) from testdb.table_1 where Latitude between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' and Age between '+request.form.get('age_1')+' and '+request.form.get('age_2')+' ; ')
    #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
    #result1 = cursor.fetchall()

    beforeTime = time.time()
    for x in range(1, int(request.form.get('count'))):
        rand_number = random.randrange(0, int(request.form.get('count')))
        #rand_number = request.form.get('count')
        sql = 'select latitude, longitude, place ,time from tableName where time between '+request.form.get('lat_1')+' or '+request.form.get('lat_2')+' LIMIT {}; '.format(rand_number)
        print("SQL2: ",sql)
        #sql = 'select latitude, longitude, place ,time from tableName where time between '+request.form.get('lat_1')+' and '+request.form.get('lat_2')+' LIMIT '+ (rand_number)+';'
        cursor.execute(sql)
        #cursor.execute('SELECT GivenName, City, State FROM testdb.table_1 where city like \'%' + request.form.get('city') + '\' ;')
        result = cursor.fetchall()
        print( str(x) +' : '+ str(len(result)))
        afterTime = time.time()
        timeDifference = afterTime - beforeTime
    return render_template('query4.html', time=timeDifference,query1 = sql)
    
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=6600, threaded=True,debug=True)



