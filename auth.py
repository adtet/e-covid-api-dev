import flask
import mysql.connector
from flask import Flask, jsonify, request
import uuid
import base64
import hashlib
import json
import datetime
from datetime import date
import calendar
from waitress import serve
app = Flask(__name__)


@app.route("/auth/regist", methods=['POST'])
def regist():
    json_data = flask.request.json
    if json_data == None:
        result = {"message": "Process Failed"}
        resp.status_code = 400
        resp = jsonify(result)
        return resp
    else:
        if 'nim' not in json_data and 'username' not in json_data and 'prodi' not in json_data and 'kelas' not in json_data and 'email' not in json_data and 'password' not in json_data:
            result = {"message": "error request"}
            resp = jsonify(result)
            resp.status_code = 401
        else:
            nim = json_data['nim']
            username = json_data['username']
            jurusan = json_data['jurusan']
            prodi = json_data['prodi']
            kelas = json_data['kelas']
            email = json_data['email']
            paswd = json_data['password']
            id = str(uuid.uuid4().hex)
            password = hashlib.sha512(paswd.encode()).hexdigest()
            cek = cek_siswa(nim, username)
            if cek == 0:
                result = {"message": "Already registered"}
                resp = jsonify(result)
                resp.status_code = 201
                return resp
            else:
                input_regist(id, nim, username, jurusan, prodi, kelas, email,
                             password)
                result = {"message": "Regist success"}
                resp = jsonify(result)
                resp.status_code = 200
                return resp


def sql_connection():
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 password="",
                                 database="db_coba")
    return db


def cek_siswa(a, b):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM user_regist where nim=%s and username=%s",
                   (a, b))
    c = cursor.fetchone()
    if c == None:
        return 0
    else:
        return 1


def input_regist(a, b, c, d, e, f, g, h):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO user_regist (id,nim,username,jurusan,prodi,kelas,email,pass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        (a, b, c, d, e, f, g, h))
    db.commit()