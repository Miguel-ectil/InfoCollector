import requests
import sqlite3

def buscar_dados_pais(nome_pais):
    url = f"https://restcountries.com/v3.1/name/{nome_pais}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()[0]  
        print(f"Dados encontrados para '{nome_pais}': {dados}")
        pais = {
            "nome": dados.get("name", {}).get("common", ""),
            "capital": dados.get("capital", [""])[0],
            "regiao": dados.get("region", ""),
            "subregiao": dados.get("subregion", ""),
            "populacao": dados.get("population", 0),
            "area": dados.get("area", 0),
            "moeda": list(dados.get("currencies", {}).keys())[0] if dados.get("currencies") else "",
            "idioma": list(dados.get("languages", {}).values())[0] if dados.get("languages") else ""
        }
    except Exception as e:
        print(f"Erro ao buscar dados para '{nome_pais}': {e}")
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