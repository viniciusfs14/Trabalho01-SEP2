import pandas as pd


def verificar_limites_tensao(barras, V, vmin=0.95, vmax=1.05):
    resultados = []

    for i, barra in barras.iterrows():
        tensao = V[i]

        if tensao < vmin:
            status = "VIOLADO - SUBTENSÃO"
        elif tensao > vmax:
            status = "VIOLADO - SOBRETENSÃO"
        else:
            status = "OK"

        resultados.append({
            "barra": int(barra["barra"]),
            "tipo": barra["tipo"],
            "V": tensao,
            "Vmin": vmin,
            "Vmax": vmax,
            "status": status
        })

    return pd.DataFrame(resultados)


def verificar_limites_geracao(barras, Pcalc):
    resultados = []

    for i, barra in barras.iterrows():
        if barra["tipo"] not in ["PV", "SW"]:
            continue

        Pg = Pcalc[i] + barra["PD"]
        Pgmin = barra["CGmin"]
        Pgmax = barra["CGmax"]

        if Pg < Pgmin:
            status = "VIOLADO - GERAÇÃO ABAIXO DO MÍNIMO"
        elif Pg > Pgmax:
            status = "VIOLADO - GERAÇÃO ACIMA DO MÁXIMO"
        else:
            status = "OK"

        resultados.append({
            "barra": int(barra["barra"]),
            "tipo": barra["tipo"],
            "Pg": Pg,
            "Pgmin": Pgmin,
            "Pgmax": Pgmax,
            "status": status
        })

    return pd.DataFrame(resultados)


def verificar_limites_circuitos(fluxos):
    resultados = []

    for _, linha in fluxos.iterrows():
        carregamento = max(linha["Skm"], linha["Smk"])
        cap = linha["cap"]

        if carregamento > cap:
            status = "VIOLADO - SOBRECARGA"
        else:
            status = "OK"

        resultados.append({
            "de": int(linha["de"]),
            "para": int(linha["para"]),
            "ncir": int(linha["ncir"]),
            "Skm": linha["Skm"],
            "Smk": linha["Smk"],
            "carregamento": carregamento,
            "cap": cap,
            "uso_%": 100 * carregamento / cap,
            "status": status
        })

    return pd.DataFrame(resultados)