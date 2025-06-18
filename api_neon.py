from fastapi import FastAPI
import psycopg2

app = FastAPI(
    title="Quitzau API",
    description="API de produtos conectada ao banco Neon, retorna todos os produtos",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

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
        {
            "codigo": row[0],
            "descricao": row[1],
            "custo": float(row[2])
        }
        for row in resultados
    ]
