import pandas as pd


def ler_dados_sistema(nome_arquivo):
    with open(nome_arquivo, "r", encoding="latin-1") as arquivo:
        linhas = arquivo.readlines()

    dados_barras = []
    dados_circuitos = []

    lendo_dbar = False
    lendo_dcir = False

    for linha in linhas:
        linha = linha.strip()

        if linha == "DBAR":
            lendo_dbar = True
            lendo_dcir = False
            continue

        if linha == "DCIR":
            lendo_dbar = False
            lendo_dcir = True
            continue

        if linha.startswith("####"):
            lendo_dbar = False
            lendo_dcir = False
            continue

        if not linha or linha.startswith("x---") or linha.startswith("BARRA") or linha.startswith("BDE"):
            continue

        partes = linha.split()

        if lendo_dbar:
            dados_barras.append({
                "barra": int(partes[0]),
                "PD": float(partes[1]),
                "QD": float(partes[2]),
                "Bsh": float(partes[3]),
                "tipo": partes[4],
                "Vesp": float(partes[5]),
                "Oesp": float(partes[6]),
                "PGesp": float(partes[7]),
                "custo": float(partes[8]),
                "CGmin": float(partes[9]),
                "CGmax": float(partes[10])
            })

        elif lendo_dcir:
            dados_circuitos.append({
                "de": int(partes[0]),
                "para": int(partes[1]),
                "ncir": int(partes[2]),
                "r": float(partes[3]),
                "x": float(partes[4]),
                "bsh": float(partes[5]),
                "tap": float(partes[6]),
                "defasagem": float(partes[7]),
                "estado": partes[8],
                "cap": float(partes[9])
            })

    barras = pd.DataFrame(dados_barras)
    circuitos = pd.DataFrame(dados_circuitos)

    return barras, circuitos