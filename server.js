const express = require("express");
const axios = require("axios");
const mysql = require("mysql");

const app = express();
const PORT = process.env.PORT || 3078;
const url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json";

// Configuração para conexão com o banco de dados MySQL
const connection = mysql.createConnection({
  host: "7875",
  user: "mega",
  password: "megamega",
  database: "OCPDB755"
});

// Função para criar a tabela no banco de dados se ainda não existir
function criarTabela() {
  const query = `
    CREATE TABLE IF NOT EXISTS cotacao_dolar (
      id INT AUTO_INCREMENT PRIMARY KEY,
      valor DECIMAL(10, 2),
      data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `;
  
  connection.query(query, (error) => {
    if (error) {
      console.error("Erro ao criar a tabela no banco de dados:", error);
    } else {
      console.log("Tabela criada com sucesso (ou já existente).");
    }
  });
}

// Função para obter a cotação do dólar e salvar no banco de dados
async function obterCotacaoDolar() {
  try {
    const response = await axios.get(url);
    const dados = response.data;
    const dataAtual = new Date().toISOString().slice(0, 19).replace('T', ' ');

    let valorEncontrado = null;

    for (let i = 0; i < dados.length; i++) {
      if (dataAtual === dados[i].data) {
        valorEncontrado = dados[i].valor;
        break;
      } 
    }

    if (valorEncontrado !== null) {
      const query = `INSERT INTO cotacao_dolar (valor) VALUES (${valorEncontrado})`;
      
      connection.query(query, (error) => {
        if (error) {
          console.error("Erro ao inserir a cotação no banco de dados:", error);
        } else {
          console.log("Cotação inserida no banco de dados com sucesso.");
        }
      });
    } else {
      console.log("Cotação não encontrada para a data atual.");
    }
  } catch (error) {
    console.error("Erro ao obter a cotação:", error);
  }
}

// Inicialização: criação da tabela e início da obtenção periódica da cotação
criarTabela();
setInterval(obterCotacaoDolar, 5000);

// Inicia o servidor Express
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});







