# /usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request,jsonify
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'huawei_db'

mysql.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        json_obj = json.loads(json.dumps(request.json))
        full_name = json_obj["full_name"]
        login = json_obj["login"]
        password = json_obj["password"]
        number_phone = json_obj["number_phone"]
        model_phone = json_obj["model_phone"]
        email = None
        if "email" in json_obj:
            email = json_obj["email"]
    except Exception:
        conn.commit()
        return jsonify(state="error",response="Error in format json")

    try:
        email_ = "NULL" if email is None else email
        cur.execute(
            '''INSERT INTO Users (full_name,login,password,number_phone,model_phone,email) VALUES ('%s','%s','%s','%s','%s','%s')'''
            % (full_name, login, password, number_phone, model_phone, email_))
        cur.execute('''SELECT id FROM Users WHERE login='%s' ''' % login)
        date = cur.fetchone()
    except Exception:
        conn.commit()
        return jsonify(state="error",response="User with this login already exists!")
    conn.commit()
    return jsonify(state="ok",response={"id": date[0]})


@app.route('/auth', methods=['GET'])
def auth():
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        login = request.args.get("login")
        password = request.args.get("password")
        if login == "" or password == "":
            raise Exception("")
    except Exception:
        conn.commit()
        return jsonify(state="error",response="Invalid login or password")

    cur.execute('''SELECT id FROM Users WHERE login='%s' AND password='%s' ''' % (login, password))
    date = cur.fetchone()
    if date is None:
        conn.commit()
        return jsonify(state="error",response="User with this login and password doesn't exist!")
    else:
        conn.commit()
        return jsonify(state="ok",response={"id": date[0]})


@app.route('/user', methods=['GET'])
def getUserByID():
    conn = mysql.connect()
    cur = conn.cursor()
    try:
        id_user = int(request.args.get("id"))
    except Exception:
        conn.commit()
        return jsonify(state="error",response="Invalid type of id")

    cur.execute('''SELECT * FROM Users WHERE id='%s' ''' % (str(id_user)))
    date = cur.fetchone()
    if date is None:
        conn.commit()
        return jsonify(state="error",response="User with this id doesn't exist!")
    else:
        conn.commit()
        return jsonify(state="ok",response={
                "id": date[0],
                "full_name": date[1],
                "login": date[2],
                "password": date[3],
                "email": date[4],
                "number_phone": date[5],
                "model_phone": date[6]
            })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int('8888'), debug=True)
