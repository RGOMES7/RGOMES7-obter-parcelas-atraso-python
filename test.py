import pytest
from app import app

# Fixture para obter um cliente_id válido para os testes
@pytest.fixture
def cliente_id():
    return 1  # Substitua com um ID válido existente no seu banco de dados

# Testar se a rota retorna um código de status 200
def test_obter_parcelas_atraso_status_code(cliente_id):
    client = app.test_client()
    response = client.get(f'/cliente/{cliente_id}/parcelas-atraso')
    assert response.status_code == 200

# Testar se a rota retorna dados JSON esperadosn
def test_obter_parcelas_atraso_json(cliente_id):
    client = app.test_client()
    response = client.get(f'/cliente/{cliente_id}/parcelas-atraso')
    json_data = response.get_json()

    assert isinstance(json_data, list)
    assert all('pagamento_id' in item and 'pedido_id' in item and 'cliente_nome' in item and 'item' in item
               and 'valor' in item and 'data_vencimento' in item for item in json_data)
