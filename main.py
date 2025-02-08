import base64
from io import BytesIO
from flask import Flask, request, jsonify
from ofxparse import OfxParser

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask OFX Parser API is running!"

@app.route('/parse_ofx', methods=['POST'])
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
                "routing_number": account.routing_number,
                "branch_id": account.branch_id,
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
            def str_to_float(value:str):
                 return float(value.replace(",", "."))
            for transaction in account.statement.transactions:
                transaction_data = {
                    "payee": transaction.payee,
                    "type": transaction.type,
                    "date": str(transaction.date),
                    "user_date": str(transaction.user_date),
                    "amount": str_to_float(str(transaction.amount)),
                    "category": str(transaction.memo).split(" - ")[0]
                    "memo": transaction.memo,
                    "describe": str(transaction.memo) + " " + str(transaction.amount),
                    "sic": transaction.sic,
                    "mcc": transaction.mcc,
                    "checknum": transaction.checknum
                }
                account_data["transactions"][transaction.id] = transaction_data
                
            result.append(account_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Executa localmente (para testes)
    # Railway definirá a porta via variável de ambiente $PORT,
    # então aqui podemos ficar fixo em 5000, pois em produção
    # o Railway já injeta esse valor.
    app.run(debug=True, port=os.getenv("PORT", default=5000))
