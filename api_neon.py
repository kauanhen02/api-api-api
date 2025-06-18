from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="ep-silent-moon-acmr3exh-pooler.sa-east-1.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_P3VoRfX0uUqk",
        port=5432,
        sslmode="require"
    )

@app.get("/produtos")
def listar_todos_produtos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT pro_in_codigo, pro_st_descricao, re_custo
        FROM produtos
    """)
    
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"codigo": r[0], "descricao": r[1], "custo": float(r[2])} for r in resultados
    ]
