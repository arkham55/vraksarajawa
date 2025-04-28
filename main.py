import firebase_admin
from firebase_admin import credentials, db
from fastapi import FastAPI
import mysql.connector
from pydantic import BaseModel

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("D:\MPPL\Backend\mppl-backend-firebase-adminsdk-fbsvc-4d5fcad3fa.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mppl-backend-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

db_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vraksarajawa"
)
cursor = db_mysql.cursor()

app = FastAPI()

app = FastAPI()

# Definisi request body
class Result(BaseModel):
    user_id: str
    level: str
    latihan_type: str
    score: int
    correct_answers: int

@app.post("/submit-result/")
async def submit_result(result: Result):
    # Untuk debug dulu, print semua isi body
    print(result)

    # Contoh proses (nanti ganti ini update ke Firebase dan MySQL)
    return {"message": "Data diterima", "data": result}
    
    # 2. Simpan ke MySQL
    sql = "INSERT INTO assessment_results (user_id, level, latihan_type, score, correct_answers, total_questions) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (user_id, level, latihan_type, score, correct_answers, 5)
    cursor.execute(sql, val)
    db_mysql.commit()
    
    return {"status": "success"}

@app.get("/get-progress/{user_id}")
async def get_progress(user_id: str):
    ref = db.reference(f'users/{user_id}/progress')
    progress_data = ref.get()
    if progress_data is None:
        return {"message": "Progress not found", "user_id": user_id}
    return {"user_id": user_id, "progress": progress_data}

cursor = db_mysql.cursor(dictionary=True)  # pakai dictionary untuk hasil rapi

@app.get("/get-assessment/{user_id}")
async def get_assessment(user_id: str):
    cursor.execute("SELECT * FROM assessment_results WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    if not results:
        return {"message": "No assessment data found", "user_id": user_id}
    return {"user_id": user_id, "assessments": results}
