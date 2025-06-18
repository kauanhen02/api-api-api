from fastapi import FastAPI
import psycopg2

app = FastAPI(
    title="Quitzau API",
    description="API de produtos conectada ao banco Neon com filtro fixo para BAMBOO",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"  # Necessário para o ChatGPT reconhecer
)

# Função para conectar ao banco PostgreSQL da Neon
def get_conn():
    return psycopg2.connect(
        host="ep-silent-moon-acmr3exh-pooler.sa-east-1.aws.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_P3VoRfX0uUqk",
        port=5432,
        sslmode="require"
    )

# Endpoint que retorna os produtos com descrição "BAMBOO"
@app.get("/produtos")
def listar_produtos_bamboo():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT pro_in_codigo, pro_st_descricao, re_custo
        FROM produtos
        WHERE pro_st_descricao ILIKE 'BAMBOO'
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
