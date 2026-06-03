from flask import Flask, jsonify, request
import time, requests, os, pymysql
from jose import jwt

# Backend dùng tên nội bộ Docker để fetch JWKS (port 8080)
_INTERNAL = os.getenv("OIDC_INTERNAL", "http://authentication-identity-server:8080")
REALM     = os.getenv("OIDC_REALM",    "realm_52300263")
AUDIENCE  = os.getenv("OIDC_AUDIENCE", "account")
JWKS_URL  = f"{_INTERNAL}/realms/{REALM}/protocol/openid-connect/certs"

_JWKS = None; _TS = 0
def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = now
    return _JWKS

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host='relational-database-server',
        user='root',
        password='root',
        database='studentdb',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")

@app.get("/students-db")
def students_db():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM students')
            rows = cur.fetchall()
    finally:
        conn.close()

    html = """
    <html><head><style>
        body { font-family: Arial; padding: 20px; }
        h2 { color: #2e7d32; }
        table { border-collapse: collapse; width: 100%; }
        th { background: #2e7d32; color: white; padding: 10px; text-align: left; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        tr:hover { background: #f5f5f5; }
    </style></head><body>
    <h2>Danh sách sinh viên (MariaDB)</h2>
    <table>
        <tr><th>#</th><th>Student ID</th><th>Fullname</th><th>DOB</th><th>Major</th></tr>
    """
    for i, r in enumerate(rows, 1):
        html += f"<tr><td>{i}</td><td>{r['student_id']}</td><td>{r['fullname']}</td><td>{r['dob']}</td><td>{r['major']}</td></tr>"
    html += "</table></body></html>"
    return html

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], audience=AUDIENCE, options={"verify_iss": False})
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"), email=payload.get("email"))
    except Exception as e:
        return jsonify(error=str(e)), 401


# Thêm code ở đây:
import json

@app.get("/student")
def student():
    with open("students.json") as f:
        data = json.load(f)
    return jsonify(data)
# Kết thúc code thêm vào

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)


