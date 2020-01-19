from flask import Flask,redirect,url_for,render_template,jsonify,json,request
from flask_pymongo import PyMongo
import pandas as pd
import ast
from bson import json_util,ObjectId

app =Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskApp"
mongo = PyMongo(app)

#Read data
@app.route('/')
def hello():
    data=mongo.db.movie.find_one()
    return render_template('index.html',data=data['name'])


@app.route('/data/<id>',methods=['GET','POST','DELETE','PUT'])
def insert_data(id):
    try:
        if request.method=='GET':
            data = mongo.db.movies.find()
            print('data ',data)
            return json_util.dumps(data)

        if request.method=='POST':
            data=json.loads(request.data)
            mongo.db.movies.insert_many(data);
            return "Data inserted successfully"

        if request.method=='DELETE':
            print('id====> ',id)
            del_data={"_id": ObjectId(id)}
            mongo.db.movies.delete_one(del_data)
            return 'Delted successfully'

        if request.method=='PUT':
            upQuery={"_id":ObjectId(id)}
            data = json.loads(request.data)
            valQuery={"$set":data}
            mongo.db.movies.update_one(upQuery,valQuery);
            return "Movie updated successfully"

    except (ValueError,TypeError,KeyError,SyntaxError) as e:
        print('Err ',e)


# def excelRead():
#     df=pd.read_excel('test.xlsx',orient='records').to_json()
#     data=ast.literal_eval(df)
#     # print(data['name'])
#     val=mongo.db.movies.find()
#     for val in val:
#         print(val)

if __name__=='__main__':
    app.run(debug=True)