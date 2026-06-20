from flask import Flask,jsonify,request
import sqlite3
def init_db():
    conn = sqlite3.connect("experiment_db.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS navodayans (
            serial_no INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Batch INTEGER
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM navodayans")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO navodayans (Name,Batch)
            VALUES('Kumar Rudra Raj',2024)
        """)
    conn.commit()
    conn.close()

init_db()
app = Flask(__name__)
@app.route('/view_jnvbgs/<category>',methods = ["GET"])
def get_info(category):
    conn = sqlite3.connect("experiment_db.db")
    cursor = conn.cursor()
    cursor.execute("SELECT serial_no,Name,Batch FROM navodayans WHERE Name = ?",(category,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    if row:
        return jsonify({
            "serial_no.": row[0],
            "Name": row[1],
            "Batch": row[2]
        })
    return ("error: Not Found"),404

@app.route('/view_jnvbgs',methods = ["POST"])
def register():
    incoming_data = request.json
    Name = incoming_data.get("Name","unknown_scholar")
    Batch = incoming_data.get("Batch")
    conn = sqlite3.connect("experiment_db.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO navodayans ("Name","Batch")
        VALUES(?,?)
    """,(Name,Batch))
    conn.commit()
    conn.close()
    return jsonify({
        "Status": "Success",
        "Confirmation": "Registration done successfully"
    }),201

@app.route('/view_jnvbgs/<int:sno>',methods = ["PUT"])
def update_info(sno):
    incoming_data = request.json
    New_name = incoming_data.get("Name","nw_name")
    New_batch = incoming_data.get("Batch")
    conn = sqlite3.connect("experiment_db.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE navodayans
        SET Name = ?, Batch = ?
        WHERE serial_no = ?
    """,(New_name,New_batch,sno))
    conn.commit()
    conn.close()
    return jsonify({
        "Status": "Success",
        "Confirmation":"Scholar info updated successfully"
    }),200

@app.route('/view_jnvbgs/<int:sno>', methods = ["DELETE"])
def del_info(sno):
    conn = sqlite3.connect("experiment_db.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM navodayans WHERE serial_no = ?",(sno,))
    conn.commit()
    conn.close()
    return jsonify({
        "Status":"Success",
        "Confirmation":"Scholar deleted from the database successfully"
    }), 200

if __name__ == "__main__":
    app.run(debug = True)

  
