from fastapi import FastAPI, Query
import psycopg2

app = FastAPI(
    title="Quitzau API",
    description="API de produtos com paginação conectada ao banco Neon",
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
def listar_produtos(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    offset = (page - 1) * page_size

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT pro_in_codigo, pro_st_descricao, re_custo
        FROM produtos
        ORDER BY pro_in_codigo
        LIMIT %s OFFSET %s
    """, (page_size, offset))

    resultados = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"codigo": r[0], "descricao": r[1], "custo": float(r[2])}
        for r in resultados
    ]
