from fastapi import FastAPI, Query
import psycopg2
import os

app = FastAPI()

# Configuração da conexão com o Neon
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
def buscar_produtos(descricao: str = Query(..., description="Descrição do produto")):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT pro_in_codigo, pro_st_descricao, re_custo
        FROM produtos
        WHERE pro_st_descricao ILIKE %s
    """, (descricao,))
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [{"codigo": r[0], "descricao": r[1], "custo": float(r[2])} for r in rows]
