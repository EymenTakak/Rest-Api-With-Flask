import sqlite3

from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn=sqlite3.connect('AriBilgi.db')
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/ogrenci', methods=["GET","POST"])
def ogrenciler():
    conn=db_connection()
    c = conn.cursor()
    if request.method == "GET":
        c.execute('SELECT * FROM ogrenciler')
        ogrenciliste = [
            dict(id=row[0], ad=row[1], soyad=row[2], telefon=row[3])
            for row in c.fetchall()
        ]
        if ogrenciliste is not None:
            return jsonify(ogrenciliste)


    if request.method == "POST":
        new_ad = request.form['ad']
        new_soyad = request.form['soyad']
        new_telefon = request.form['telefon']
        sql = "INSERT INTO ogrenciler (ad,soyad,telefon) VALUES(?,?,?)"
        c.execute(sql,(new_ad,new_soyad,new_telefon))
        conn.commit()
        return f"{c.lastrowid} numaralı Ogrenci Basariyla Olusturuldu", 201

@app.route('/ogrenci/<int:id>', methods=["GET", "PUT", "DELETE"])
def single_ogrenci(id):
    conn = db_connection()
    c = conn.cursor()
    ogrenci = None
    if request.method == 'GET':
        c.execute("SELECT * FROM ogrenciler WHERE id=?", (id,))
        rows = c.fetchall()
        for r in rows:
            ogrenci = r
        if ogrenci is not None:
            return jsonify(ogrenci), 200
        else:
            return "Bir Şeyler Ters Gitti", 404


    if request.method == 'PUT':
        sql = "UPDATE ogrenciler SET ad=?, soyad=?, telefon=? WHERE id=?"

        ad = request.form['ad']
        soyad = request.form['soyad']
        telefon= request.form['telefon']
        updated_ogrenci = {
            'id':id,
            'ad': ad,
            'soyad':soyad,
            'telefon':telefon
        }
        c.execute(sql,(ad,soyad,telefon,id))
        conn.commit()

        return jsonify(updated_ogrenci)
    if request.method == "DELETE":
        sql = "DELETE FROM ogrenciler WHERE id=?"
        c.execute(sql,(id,))
        conn.commit()
        return "{} Numaralı Öğrenci Başarı İle Silindi".format(id),200

if __name__ == '__main__':
    app.run(debug=True)