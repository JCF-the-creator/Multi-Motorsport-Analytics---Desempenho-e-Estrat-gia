import os
import json
import csv
import pdfplumber

PASTA_ALVO = r"C:\Users\Lucas\Downloads\Resultados_Rally_2025_Completo - Copia"

def limpar_e_validar_valor(valor):
    """
    Limpa o texto e remove ruídos comuns de tabelas vazias.
    Retorna "" se o campo não contiver informação útil.
    """
    if valor is None:
        return ""
    
    # Remove quebras de linha internas para não quebrar a estrutura do CSV/Excel
    v = str(valor).strip().replace('\r', '').replace('\n', ' ')
    
    # Padroniza marcas de tempo ausente ou nulo como string vazia
    if v in ["* * *", "***", "* *", "None", "-", "##:##:##", ""]:
        return ""
    return v

def detectar_header_da_pagina(tabela_da_pagina):
    """
    Inspeciona as linhas de uma tabela específica para extrair o 
    cabeçalho exclusivo dela.
    """
    palavras_chave = ["POS", "NUM", "NÃO", "NO", "PILOTO", "CAT", "TEMPO", "TOTAL"]
    
    for linha in tabela_da_pagina:
        linha_limpa = [limpar_e_validar_valor(c).upper() for c in list(linha)]
        # Se a linha contiver indicadores de cabeçalho, ela é a nossa estrutura
        if any(x in linha_limpa for x in palavras_chave):
            headers = []
            for idx, celula in enumerate(linha):
                nome = limpar_e_validar_valor(celula).upper()
                if not nome:
                    nome = f"COLUNA_{idx+1}"
                
                # Padronizações essenciais para consistência
                if nome in ["NÃO", "NO"]: nome = "NUM"
                if "PILOTO" in nome: nome = "PILOTO_INFO"
                if "TOTAL" in nome or "LIDER" in nome: nome = "TOTAL DIF.LIDER DIF.ANTERIOR"
                
                # Evita colisões de nomes na mesma página
                if nome in headers:
                    nome = f"{nome}_{idx+1}"
                headers.append(nome)
            return headers
            
    return None

def extrair_estruturas_por_pagina(caminho_pdf):
    """
    Varre o PDF inspecionando e tratando cada página como uma estrutura única.
    """
    dados_finais = []
    cabecalho_meta = {
        "COMPETICAO": "Rally Barretos 2025",
        "ARQUIVO_ORIGEM": os.path.basename(caminho_pdf)
    }
    
    with pdfplumber.open(caminho_pdf) as pdf:
        if not pdf.pages:
            return None
            
        # Captura os metadados textuais do topo da primeira página apenas
        texto_p1 = pdf.pages[0].extract_text() or ""
        linhas_p1 = [l.strip() for l in texto_p1.split('\n') if l.strip()]
        meta_texto = []
        for l in linhas_p1:
            if any(x in l.upper() for x in ["POS", "NUM", "PILOTO", "CHRONOSAT"]):
                break
            meta_texto.append(l)
        cabecalho_meta["INFO_GERAL"] = " | ".join(meta_texto)

        # LOOP INDIVIDUAL: Cada página é analisada isoladamente
        for num_pag, pagina in enumerate(pdf.pages):
            tabelas = pagina.extract_tables()
            if not tabelas:
                continue
                
            for tabela in tabelas:
                if not tabela:
                    continue
                
                # 1. Descobre a estrutura de colunas EXCLUSIVA desta página
                headers_da_pagina = detectar_header_da_pagina(tabela)
                
                # 2. Se a página não tiver cabeçalho explícito, cria um dinâmico baseado na largura da linha
                if not headers_da_pagina:
                    largura_maxima = max(len(linha) for linha in tabela)
                    headers_da_pagina = [f"COL_{i+1}" for i in range(largura_maxima)]
                
                # 3. Extrai os dados baseando-se estritamente no mapeamento desta folha
                for linha in tabela:
                    linha_limpa = [limpar_e_validar_valor(c) for c in linha]
                    
                    # Ignora linhas totalmente vazias ou que sejam a própria linha de cabeçalho
                    if all(c == "" for c in list(linha_limpa)):
                        continue
                    if any(x in [str(c).upper() for c in linha_limpa] for x in ["POS", "PILOTO/NAVEGADOR", "CHRONOSAT"]):
                        continue
                        
                    registro = {}
                    for idx, valor in enumerate(linha_limpa):
                        # REGRA ATENDIDA: Se o dado for vazio "", ignora e NÃO cria a chave no JSON
                        if valor == "":
                            continue
                            
                        # Associa a chave correspondente à coluna da página atual
                        if idx < len(headers_da_pagina):
                            chave = headers_da_pagina[idx]
                        else:
                            chave = f"EXTRA_COL_{idx+1}"
                            
                        registro[chave] = valor
                        
                    # Só adiciona o registro se ele contiver dados mínimos de identificação do piloto
                    if registro and any(k in registro for k in ["POS", "NUM", "PILOTO_INFO", "COL_1", "COL_2"]):
                        dados_finais.append(registro)
                        
    return {"CABECALHO": cabecalho_meta, "DADOS": dados_finais}

def main():
    print(f"🚀 Iniciando Auditoria Estrutural Individual por Página em:\n -> {PASTA_ALVO}\n")
    
    if not os.path.exists(PASTA_ALVO):
        print("[!] Erro: A pasta especificada não existe.")
        return

    arquivos_processados = 0
    
    for raiz, _, arquivos in os.walk(PASTA_ALVO):
        for arquivo in arquivos:
            if arquivo.lower().endswith('.pdf'):
                caminho_pdf = os.path.join(raiz, arquivo)
                print(f"[+] Verificando colunas e dados da página de: {arquivo}")
                
                estrutura = extrair_estruturas_por_pagina(caminho_pdf)
                
                if not estrutura or not estrutura["DADOS"]:
                    print(f"[-] Nenhum dado consistente extraído de: {arquivo}")
                    continue
                
                nome_base = os.path.splitext(caminho_pdf)[0]
                caminho_json = nome_base + ".json"
                caminho_csv = nome_base + ".csv"
                
                # 1. Salva o JSON dinâmico livre de chaves vazias
                with open(caminho_json, 'w', encoding='utf-8') as f:
                    json.dump(estrutura, f, indent=4, ensure_ascii=False)
                    
                # 2. Varre as chaves que REALMENTE sobreviveram para montar as colunas do CSV
                chaves_reais = []
                for reg in estrutura["DADOS"]:
                    for k in reg.keys():
                        if k not in chaves_reais:
                            chaves_reais.append(k)
                
                # Ordenação estruturada amigável para exibição em planilhas
                ordem_ideal = ["POS", "NUM", "PILOTO_INFO", "CAT", "DIA 1", "DIA 2", "DIA 3", "TEMPO", "PENAL", "TOTAL DIF.LIDER DIF.ANTERIOR"]
                colunas_csv = [c for c in ordem_ideal if c in chaves_reais]
                colunas_csv += [c for c in chaves_reais if c not in colunas_csv]

                # 3. Grava o CSV correspondente
                with open(caminho_csv, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f, delimiter=';')
                    
                    # Adiciona metadados como comentários no topo
                    for k, v in estrutura["CABECALHO"].items():
                        writer.writerow([f"# {k}: {v}"])
                    writer.writerow([])
                    
                    dict_writer = csv.DictWriter(f, fieldnames=colunas_csv, delimiter=';')
                    dict_writer.writeheader()
                    dict_writer.writerows(estrutura["DADOS"])
                    
                arquivos_processados += 1

    print("\n" + "="*60)
    print(" 🎉 PROCESSO CONCLUÍDO!")
    print(f" -> Arquivos PDF inspecionados: {arquivos_processados}")
    print(" -> Dados nulos ou vazios foram ignorados.")
    print("="*60)

if __name__ == '__main__':
    main()
