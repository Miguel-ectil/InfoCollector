import requests
import sqlite3

def buscar_dados_pais(nome_pais):
    url = f"https://restcountries.com/v3.1/name/{nome_pais}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()[0]  # Pegamos apenas o primeiro resultado
    except Exception as e:
        print(f"Erro ao buscar dados para '{nome_pais}': {e}")
        return None
    
    try:
        nome_comum = dados['name']['common']
        nome_oficial = dados['name']['official']
        capital = dados['capital'][0] if 'capital' in dados and dados['capital'] else 'N/A'
        continente = dados.get('continents', ['N/A'])[0]
        regiao = dados.get('region', 'N/A')
        sub_regiao = dados.get('subregion', 'N/A')
        populacao = dados.get('population', 0)
        area = dados.get('area', 0.0)

        moeda_info = list(dados.get('currencies', {}).values())[0] if 'currencies' in dados else {'name': 'N/A', 'symbol': ''}
        moeda_nome = moeda_info.get('name', 'N/A')
        moeda_simbolo = moeda_info.get('symbol', '')

        idioma_info = list(dados.get('languages', {}).values())[0] if 'languages' in dados else 'N/A'
        fuso_horario = dados.get('timezones', ['N/A'])[0]
        url_bandeira = dados['flags']['png']

        return (
            nome_comum, nome_oficial, capital, continente,
            regiao, sub_regiao, populacao, area,
            moeda_nome, moeda_simbolo, idioma_info,
            fuso_horario, url_bandeira
        )
    except Exception as e:
        print(f"Erro ao processar dados de '{nome_pais}': {e}")
        return None

# Conectar ao banco SQLite e criar tabela se não existir
def criar_banco():
    conn = sqlite3.connect('paises.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_comum TEXT,
            nome_oficial TEXT,
            capital TEXT,
            continente TEXT,
            regiao TEXT,
            sub_regiao TEXT,
            populacao INTEGER,
            area REAL,
            moeda_nome TEXT,
            moeda_simbolo TEXT,
            idioma TEXT,
            fuso_horario TEXT,
            url_bandeira TEXT
        )
    ''')
    conn.commit()
    return conn, cursor    

# Coletar países do usuário
def coletar_paises():
    paises = []
    for i in range(3):
        nome = input(f"Digite o nome do {i+1}º país: ").strip()
        paises.append(nome)
    return paises

def inserir_pais(cursor, dados):
    cursor.execute('''
        INSERT INTO paises (
            nome_comum, nome_oficial, capital, continente,
            regiao, sub_regiao, populacao, area,
            moeda_nome, moeda_simbolo, idioma,
            fuso_horario, url_bandeira
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)

    
def main():
    conn, cursor = criar_banco()
    # paises = coletar_paises()

    for pais in ["Brasil", "Argentina", "Chile", "Uruguai", "Paraguai"]:
        dados = buscar_dados_pais(pais)
        if dados:
            # inserir_pais(cursor, dados)
            print(f"✅ Dados de '{pais}' inseridos com sucesso.")
        else:
            print(f"⚠️ Dados de '{pais}' não foram inseridos.")

    # conn.commit()
    # conn.close()
    print("\n🏁 Processo concluído. Dados salvos em paises.db.")

if __name__ == "__main__":
    main()