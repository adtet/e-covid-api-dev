import mysql.connector
import json


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


def cek_login_siswa(a, b):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id,kelas FROM user_regist where email=%s and pass=%s", (a, b))
    c = cursor.fetchone()
    if c == None:
        return 0
    else:
        return c


def get_kelas(a):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute("SELECT `kelas` FROM `user_regist` WHERE id=%s", (a, ))
    c = cursor.fetchone()
    if c == None:
        return 0
    else:
        return c[0]


def get_jadwal(a, b):
    db = sql_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT jamstart,menitstart,jamend,menitend,matakuliah,dosen FROM schedule WHERE kelas=%s and day=%s",
        (a, b))
    rows = [x for x in cursor]  #compare sql data to json
    cols = [x[0] for x in cursor.description]  #compare sql data to json
    datas = []  #compare sql data to json
    for row in rows:  #compare sql data to json
        data = {}  #compare sql data to json
        for prop, val in zip(cols, row):  #compare sql data to json
            data[prop] = val  #compare sql data to json
        datas.append(data)  #compare sql data to json
    dataJson = json.dumps(datas)  #compare sql data to json
    return dataJson  #compare sql data to json
