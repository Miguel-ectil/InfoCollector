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
    
def main():
    # conn, cursor = criar_banco()
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