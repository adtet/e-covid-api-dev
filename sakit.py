from sqlLib import get_email, get_jurusan, get_nim, get_prodi, get_kelas, get_username, cek_present, insert_main
import flask
from flask import Flask, jsonify, request
from waitress import serve
from datetime import date, datetime
import calendar
app = Flask(__name__)


@app.route("/user/izin", methods=['POST'])
def izin():
    json_data = flask.request.json
    if json_data == None:
        result = {"izin": "Bad Request"}
        resp = jsonify(result)
        resp.status_code = 400
        return resp
    else:
        if 'id' not in json_data or 'matakuliah' not in json_data or 'dosen' not in json_data:
            result = {"izin": "Error Request"}
            resp = jsonify(result)
            resp.status_code = 401
            return resp
        else:
            id = json_data['id']
            matakuliah = json_data['matakuliah']
            dosen = json_data['dosen']
            time = datetime.datetime.now()
            tgl = date.today()
            tgl = tgl.strftime("%d%m%Y")
            day = datetime.datetime.strptime(tgl, '%d%m%Y').weekday()
            day = calendar.day_name[day]
            day = str(day)
            day = day.lower()
            if day == 'saturday' and day == 'sunday':
                result = {"izin": "schedule not available"}
                resp = jsonify(result)
                resp.status_code = 403
                return resp
            else:
                nim = get_nim(id)
                username = get_username(id)
                jurusan = get_jurusan(id)
                prodi = get_prodi(id)
                kelas = get_kelas(id)
                email = get_email(id)
                det = time.strftime("%d-%m-%Y")
                time = time.strftime("%H:%M:%S")
                info = "sakit"
                cek = cek_present(id, matakuliah, det)
                if cek == False:
                    result = {"izin": "sudah absensi"}
                    resp = jsonify(result)
                    resp.status_code = 202
                    return resp
                else:
                    insert_main(id, nim, username, jurusan, prodi, kelas,
                                email, matakuliah, dosen, day, det, time, info)
                    result = {"izin": "proses izin berhasil"}
                    resp = jsonify(result)
                    resp.status_code = 200
                    return resp


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=4005)
    app.run(port=4005, debug=True)
