import numpy as np
import pandas as pd


def calcular_fluxos(barras, circuitos, V, ang):
    resultados = []

    mapa_barras = {
        int(barra): idx for idx, barra in enumerate(barras["barra"])
    }

    theta = np.radians(ang)
    Vc = V * np.exp(1j * theta)

    for _, circuito in circuitos.iterrows():

        if circuito["estado"] != "L":
            continue

        barra_k = int(circuito["de"])
        barra_m = int(circuito["para"])

        k = mapa_barras[barra_k]
        m = mapa_barras[barra_m]

        r = circuito["r"]
        x = circuito["x"]
        bsh = circuito["bsh"]
        tap = circuito["tap"]
        defasagem = np.radians(circuito["defasagem"])
        cap = circuito["cap"]

        z = complex(r, x)
        y = 1 / z
        ysh = 1j * bsh / 2

        a = tap * np.exp(1j * defasagem)

        Vk = Vc[k]
        Vm = Vc[m]

        Ikm = ((y + ysh) / (a * np.conj(a))) * Vk - (y / np.conj(a)) * Vm
        Imk = (y + ysh) * Vm - (y / a) * Vk

        Skm = Vk * np.conj(Ikm)
        Smk = Vm * np.conj(Imk)

        perda = Skm + Smk

        S_km_abs = abs(Skm)
        S_mk_abs = abs(Smk)

        carregamento = max(S_km_abs, S_mk_abs)

        if carregamento > cap:
            status = "VIOLADO"
        else:
            status = "OK"

        resultados.append({
            "de": barra_k,
            "para": barra_m,
            "ncir": int(circuito["ncir"]),
            "Pkm": Skm.real,
            "Qkm": Skm.imag,
            "Skm": S_km_abs,
            "Pmk": Smk.real,
            "Qmk": Smk.imag,
            "Smk": S_mk_abs,
            "Pperdas": perda.real,
            "Qperdas": perda.imag,
            "cap": cap,
            "carregamento": carregamento,
            "status": status
        })

    return pd.DataFrame(resultados)