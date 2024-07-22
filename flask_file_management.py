from flask import Flask,request,jsonify,redirect,url_for,send_file
from io import BytesIO
import requests,json
import pandas as pd

from flask import Flask
from healthcheck import HealthCheck

health = HealthCheck()




app=Flask(__name__)

# Add a flask route to expose information
app.add_url_rule('/healthcheck', 'healthcheck', view_func=lambda: health.run())

@app.get("/")
def home():
    return {"my loc":"At Home"}

@app.post("/upload")
def modify_excel():
    file=request.files['updated_accuracy']
    # print(request.files)
    # return "a"
    # file.save(file.filename)
    df = pd.read_excel(file)
    df['Total']=df.apply(lambda x: x['Total']*2,axis=1)
    # df.to_excel("modified.xlsx")
    iofile=BytesIO()
    df.to_excel(iofile,index=False)
    iofile.seek(0)
    
    # return redirect(url_for("home"))
    return send_file(iofile,
                     as_attachment=True,
                     download_name="updated_accuracy.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                     )
    
    

@app.route("/call")
def call_other():
    res=requests.get('http://192.168.29.139:1050/callpadosi').text
    
    return  res

# @app.get("/nahi")

if(__name__=="__main__"):
    app.run(host="0.0.0.0",port=5000,debug=True)