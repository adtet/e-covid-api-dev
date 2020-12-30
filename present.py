import sqlLib
from sqlLib import get_email, get_jurusan, get_kelas, get_nim, get_prodi, get_matkul, get_matkul_late, insert_main, get_username, cek_id, get_kelas, cek_present
import flask
from flask import Flask, jsonify, request
from waitress import serve
from datetime import date, datetime
import calendar
app = Flask(__name__)


@app.route('/user/absen', methods=['POST'])
def absen():
    json_data = flask.request.json
    if json_data == None:
        result = {"link": "error"}
        resp = jsonify(result)
        resp.status_code = 400
        return resp
    else:
        if 'id' not in json_data or 'matakuliah' not in json_data:
            result = {"link": "Not Available"}
            resp = jsonify(result)
            resp.status_code = 401
            return resp
        else:
            id = json_data['id']
            matkul = json_data['matakuliah']
            time = datetime.now()
            tgl = date.today()
            tgl = tgl.strftime("%d%m%Y")
            day = datetime.strptime(tgl, '%d%m%Y').weekday()
            day = calendar.day_name[day]
            day = str(day)
            day = day.lower()
            jam = int(time.hour)
            menit = int(time.minute)
            cek = cek_id(id)
            if cek == False:
                result = {"link": "id Not Available"}
                resp = jsonify(result)
                resp.status_code = 403
                return resp
            else:
                if day == 'sunday' and day == 'saturday':
                    result = {"link": "schedule not available"}
                    resp = jsonify(result)
                    resp.status_code = 204
                    return resp
                else:
                    nim = get_nim(id)
                    username = get_username(id)
                    jurusan = get_jurusan(id)
                    prodi = get_prodi(id)
                    kelas = get_kelas(id)
                    email = get_username(id)
                    det = time.strftime("%d-%m-%Y")
                    time = time.strftime("%H:%M:%S")
                    waktu = (jam * 60) + menit
                    mtkl = get_matkul(kelas, day, waktu)
                    if mtkl == 0:
                        late = get_matkul_late(kelas, day, waktu)
                        if late == 0:
                            info = "you are absent"
                            result = {"link": info}
                            resp = jsonify(result)
                            resp.status_code = 203
                            return resp
                        else:
                            info = "telat"
                            cek_late = cek_present(id, late[0], det)
                            if cek_late == True:
                                insert_main(id, nim, username, jurusan, prodi,
                                            kelas, email, late[0], late[1],
                                            day, det, time, info)
                                late = str(late[0])
                                telat = late.translate(
                                    {ord(i): None
                                     for i in '-.'})
                                tlt = "".join(telat.split())
                                data = "http://g.co/meet/" + tlt.lower()
                                result = {"link": data}
                                resp = jsonify(result)
                                resp.status_code = 200
                                return resp
                            else:
                                info = "telat"
                                late = str(late[0])
                                telat = late.translate(
                                    {ord(i): None
                                     for i in '-.'})
                                tlt = "".join(telat.split())
                                data = "http://g.co/meet/" + tlt.lower()
                                result = {"link": data}
                                resp = jsonify(result)
                                resp.status_code = 200
                                return resp
                    else:
                        if matkul == str(mtkl[0]).rstrip('\r\n'):
                            info = "hadir"
                            cek_hadir = cek_present(id, mtkl[0], det)
                            if cek_hadir == True:
                                insert_main(id, nim, username, jurusan, prodi,
                                            kelas, email, mtkl[0], mtkl[1],
                                            day, det, time, info)
                                hadir = str(mtkl[0])
                                hadir = hadir.translate(
                                    {ord(i): None
                                     for i in '-.'})
                                hdr = "".join(hadir.split())
                                data = "http://g.co/meet/" + hdr.lower()
                                result = {"link": data}
                                resp = jsonify(result)
                                resp.status_code = 200
                                return resp
                            else:
                                hadir = str(mtkl[0])
                                hadir = hadir.translate(
                                    {ord(i): None
                                     for i in '-.'})
                                hdr = "".join(hadir.split())
                                data = "http://g.co/meet/" + hdr.lower()
                                result = {"link": data}
                                resp = jsonify(result)
                                resp.status_code = 200
                                return resp
                        else:
                            late = get_matkul_late(kelas, day, waktu)
                            if late == 0:
                                info = "you are absent"
                                result = {"link": info}
                                resp = jsonify(result)
                                resp.status_code = 207
                                return resp
                            else:
                                if matkul == str(late[0]).rstrip('\r\n'):
                                    cek_late = cek_present(id, late[0], det)
                                    if cek_late == True:
                                        insert_main(id, nim, username, jurusan,
                                                    prodi, kelas, email,
                                                    late[0], late[1], day, det,
                                                    time, info)
                                        late = str(late[0])
                                        telat = late.translate(
                                            {ord(i): None
                                             for i in '-.'})
                                        tlt = "".join(telat.split())
                                        data = "http://g.co/meet/" + tlt.lower(
                                        )
                                        result = {"link": data}
                                        resp = jsonify(result)
                                        resp.status_code = 200
                                        return resp
                                    else:
                                        late = str(late[0])
                                        telat = late.translate(
                                            {ord(i): None
                                             for i in '-.'})
                                        tlt = "".join(telat.split())
                                        data = "http://g.co/meet/" + tlt.lower(
                                        )
                                        result = {"link": data}
                                        resp = jsonify(result)
                                        resp.status_code = 200
                                        return resp
                                else:
                                    info = "you are absent"
                                    result = {"link": info}
                                    resp = jsonify(result)
                                    resp.status_code = 208
                                    return resp


if __name__ == "__main__":
    # serve(app, host="0.0.0.0", port=4003)
    app.run(port=4003, debug=True)
