from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
import pymysql
import pandas as pd


app = Flask(__name__)
app.config.from_object(Config)

db = pymysql.connect(
    host='127.0.0.1',
        user='root',
        password='szw970727',
        database="dha",
        cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()


@app.route("/")
def hello_world():
    return render_template("homePage.html")


@app.route("/dashboard/<study_name>")
def dashboard_detail(study_name):
    return "%s Data Dashboard" %study_name


@app.route("/study/<study_name>")
def study_detail(study_name):
    return "%s Data Dashboard" %study_name

@app.route('/site/detail')
def site_list():
    site = request.args.get("site",default="nola",type=str)
    return site

@app.route('/sum')
def site_detail():
    cursor.execute('SELECT * FROM dha.patient_imaging')
    collection_result = cursor.fetchall()
    df1 = pd.DataFrame(collection_result)
    data1 = df1.reset_index(drop=True)

    query2 = "select * from imagecollection_imaging left join wounds_imaging on imagecollection_imaging.WOUNDID = wounds_imaging.WOUNDID left join patient_imaging on wounds_imaging.PID = patient_imaging.PID"
    cursor.execute(query2)
    collection_result2 = cursor.fetchall()
    df2 = pd.DataFrame(collection_result2)
    # df2.to_excel("/Users/ziweishi/Desktop/dha.xlsx")
    data2 = df2.reset_index(drop=True)
    tables = [data1,data2]
    table_forms = [table.to_html(
        classes='table custom-style', index=False, border=2) for table in tables]


    return render_template("site_detail.html",results=table_forms)

@app.route('/sum1')
def site_detailq():
    query1 = "select * from imagecollection_imaging left join wounds_imaging on imagecollection_imaging.WOUNDID = wounds_imaging.WOUNDID left join patient_imaging on wounds_imaging.PID = patient_imaging.PID"
    cursor.execute(query1)
    collection_result = cursor.fetchall()
    df = pd.DataFrame(collection_result)
    data = df.reset_index(drop=True)
    return render_template("site_detail.html",results=data.to_html(
        classes='table custom-style',index=False,border=2))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3306, debug=True)
