import sqlLib
from sqlLib import get_email, get_jurusan, get_kelas, get_nim, get_prodi, get_matkul, get_matkul_late, insert_main
import flask
from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/user/absen', methods=['POST'])
def absen():
    a = flask.request.json


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=4003)
    app.run(port=4003, debug=True)
