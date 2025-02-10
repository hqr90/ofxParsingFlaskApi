import base64
import os
from io import BytesIO
from functools import wraps
from flask import Flask, request, jsonify
from ofxparse import OfxParser

app = Flask(__name__)

# ------------------------------------------
# Definição da SECRET KEY (token de acesso)
# ------------------------------------------
# Em produção (por exemplo, no Railway), defina a variável de ambiente MY_SECRET_TOKEN
# através do painel de configurações. Dessa forma, o valor será injetado no ambiente.
MY_SECRET_TOKEN = os.getenv("MY_SECRET_TOKEN")
if not MY_SECRET_TOKEN:
    raise Exception("A variável de ambiente MY_SECRET_TOKEN não foi definida. Configure-a no Railway.")

# ------------------------------------------
# Decorador para exigir o token no cabeçalho
# ------------------------------------------
def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Pega o token que vem no cabeçalho "X-API-KEY"
        token = request.headers.get("X-API-KEY")
        # Verifica se está presente e se é igual ao configurado
        if not token or token != MY_SECRET_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        # Se estiver tudo certo, executa a função original
        return func(*args, **kwargs)
    return wrapper

# Rota inicial só para teste
@app.route('/')
def index():
    return "Flask OFX Parser API is running!"

# ------------------------------------------
# Rota protegida por token
# ------------------------------------------
@app.route('/parse_ofx', methods=['POST'])
@require_auth  # <--- Aqui aplicamos a verificação
def parse_ofx():
    """
    Espera um JSON com a seguinte estrutura:
    {
      "ofx_base64": "STRING_BASE64_DO_ARQUIVO_OFX"
    }
    """
    data = request.get_json()
    if not data or 'ofx_base64' not in data:
        return jsonify({"error": "Campo 'ofx_base64' não encontrado no JSON"}), 400

    ofx_base64 = data['ofx_base64']

    try:
        # Decodifica o Base64 em bytes
        ofx_bytes = base64.b64decode(ofx_base64)

        # Faz o parse do OFX
        with BytesIO(ofx_bytes) as fileobj:
            ofx = OfxParser.parse(fileobj)

        # A resposta final de todos os dados
        result = []

        # Em alguns casos, ofx.accounts é uma lista de várias contas
        # Se for apenas uma, pode ser ofx.account (dependendo da versão do ofxparse).
        for account in ofx.accounts:
            account_data = {
                "account_id": account.account_id,
                "institution": {
                    "organization": account.institution.organization if account.institution else None,
                    "fid": account.institution.fid if account.institution else None
                },
                "statement": {
                    "start_date": str(account.statement.start_date),
                    "end_date": str(account.statement.end_date),
                    "balance": account.statement.balance,
                },
                "transactions": {}
            }

            # Função auxiliar para converter string em float
            def str_to_float(value: str):
                return float(value.replace(",", "."))

            for transaction in account.statement.transactions:
                transaction_data = {
                    "date": str(transaction.date),
                    "amount": str_to_float(str(transaction.amount)),
                    "category": str(transaction.memo).split(" - ")[0],
                    "memo": transaction.memo,
                }
                account_data["transactions"][transaction.id] = transaction_data

            result.append(account_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Em produção (Railway), a variável de ambiente PORT é injetada automaticamente.
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
