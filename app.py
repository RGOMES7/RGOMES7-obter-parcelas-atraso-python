from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configurações do banco de dados (substitua conforme necessário)
db_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '123456'
}


# Rota para obter as parcelas em atraso para um cliente específico
@app.route('/cliente/<int:cliente_id>/parcelas-atraso', methods=['GET'])
def obter_parcelas_atraso(cliente_id):
    # Conectar ao banco de dados
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Consulta SQL para obter as parcelas em atraso para um cliente específico
    query = sql.SQL("""
        SELECT p.id AS pagamento_id, pe.id AS pedido_id, c.nome AS cliente_nome,
               pe.item, p.valor, p.data_vencimento
        FROM cliente c
        INNER JOIN pedido pe ON c.id = pe.cliente_id
        INNER JOIN pagamento p ON pe.id = p.pedido_id
        WHERE c.id = %s AND p.foi_pago = FALSE AND p.data_vencimento < CURRENT_DATE
    """)

    # Executar a consulta com o ID do cliente como parâmetro
    cursor.execute(query, (cliente_id,))

    # Obter os resultados
    resultados = cursor.fetchall()

    # Fechar o cursor e a conexão
    cursor.close()
    conn.close()

    # Converter os resultados para um formato JSON
    resultado_json = []
    for row in resultados:
        resultado_json.append({
            'pagamento_id': row[0],
            'pedido_id': row[1],
            'cliente_nome': row[2],
            'item': row[3],
            'valor': row[4],
            'data_vencimento': row[5].isoformat()  # Converte a data para formato ISO
        })

    return jsonify(resultado_json)

# Executar o servidor
if __name__ == '__main__':
    app.run(debug=True)
