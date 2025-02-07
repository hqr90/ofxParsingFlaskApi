# OfxParsingFlaskApi

[![Licença](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  [![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/en/2.3.x/)
[![OFXParse](https://img.shields.io/badge/OFXParse-0.x-orange.svg)](https://pypi.org/project/ofxparse/)

**Uma API REST para facilitar a sua vida com arquivos OFX!**  Cansado de lidar com extratos bancários confusos?  `ofxParsingFlaskApi` transforma seus arquivos OFX em um JSON estruturado e fácil de usar.

## 🚀 Funcionalidades

* **Parseamento rápido e preciso:**  Extrai informações cruciais de arquivos OFX, como dados de contas, transações e saldos.
* **Formato JSON:**  Dados organizados e prontos para serem consumidos por qualquer aplicação.
* **Fácil de usar:**  Uma única rota (`/parse_ofx`) para processar seus arquivos OFX.
* **Código aberto:**  Contribua, modifique e personalize a API para suas necessidades!

## ⚙️ Instalação

1. Clone este repositório: `git clone https://github.com/hqr90/ofxParsingFlaskApi.git`
2. Crie um ambiente virtual (recomendado): `python3 -m venv venv`
3. Ative o ambiente virtual: `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`

## 💻 Como usar

Envie um arquivo OFX codificado em Base64 para a rota `/parse_ofx` via método POST, dentro de um JSON:

```json
{
  "ofx_base64": "STRING_BASE64_DO_SEU_ARQUIVO_OFX"
}
````

## Exemplo de resposta

```json
[
  {
    "account_id": "123456789",
    "routing_number": "987654321",
    "branch_id": "1234",
    "institution": {
        "organization": "Banco Exemplo",
        "fid": "123"
    },
    "statement": {
        "start_date": "2024-07-26",
        "end_date": "2024-08-26",
        "balance": 1000.00
    },
    "transactions": [
      {
        "payee": "Mercado da Esquina",
        "type": "DEBIT",
        "date": "2024-08-20",
        "user_date": "2024-08-20",
        "amount": -25.50,
        "id": "12345",
        "memo": "Compra no mercado",
        "sic": null,
        "mcc": null,
        "checknum": null
      },
      // ... mais transações
    ]
  }
  // ... mais contas (se houver)
]
```

## 🚀 Executando localmente

```bash
python app.py
```

A API estará disponível em `http://0.0.0.0:5000/`.

## 🐳 Deploy no Railway

O deploy no Railway é simples\! Basta conectar seu repositório. A variável de ambiente `PORT` será automaticamente configurada.

## 🤝 Contribuições

Sinta-se à vontade para abrir issues e enviar pull requests\!

## 📄 Licença

MIT License. Veja o arquivo [LICENSE](https://www.google.com/url?sa=E&source=gmail&q=LICENSE) para mais detalhes. \`\`\`

**Melhorias:**

  * **Badges:** Adicionei badges para indicar a licença (se você criar uma), versão do Python, Flask e ofxparse. Isso dá uma visão rápida das tecnologias utilizadas.
  * **Descrição Atraente:** A descrição inicial agora é mais chamativa e explica o problema que a API resolve.
  * **Destaque das Funcionalidades:** As funcionalidades principais estão listadas de forma clara.
  * **Instalação Detalhada:** Os passos de instalação são mais completos, incluindo a criação do ambiente virtual.
  * **Exemplo Completo:** O exemplo de requisição e resposta é mais detalhado, mostrando a estrutura completa do JSON.
  * **Instruções de Execução:** Adicionei instruções de como executar a API localmente.
  * **Deploy no Railway:** Mencionei a facilidade de deploy no Railway.
  * **Incentivo à Contribuição:**  Incentivei as pessoas a contribuírem com o projeto.
  * **Licença:** Adicionei uma menção à licença (e um link para o arquivo LICENSE, se você o criar).

Com este README mais completo, seu repositório ficará muito mais atrativo e fácil de usar\!
