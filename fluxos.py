import numpy as np
import pandas as pd


def calcular_fluxos(barras, circuitos, V, ang):
    resultados = []

    mapa_barras = {
        int(barra): idx for idx, barra in enumerate(barras["barra"])
    }

    theta = np.radians(ang)

    for _, circuito in circuitos.iterrows():

        if circuito["estado"] != "L":
            continue

        barra_m = int(circuito["de"])
        barra_n = int(circuito["para"])

        m = mapa_barras[barra_m]
        n = mapa_barras[barra_n]

        r = circuito["r"]
        x = circuito["x"]
        bsh_total = circuito["bsh"]
        tap = circuito["tap"]
        fi = - np.radians(circuito["defasagem"])
        cap = circuito["cap"]

        if tap == 0:
            tap = 1.0

        z = complex(r, x)
        y = 1 / z

        g = y.real
        b = y.imag

        bsh_each = bsh_total / 2

        delta_mn = theta[m] - theta[n] - fi
        delta_nm = -delta_mn

        Pmn = (V[m] ** 2 / tap ** 2) * g - (V[m] * V[n] / tap) * (
            g * np.cos(delta_mn) + b * np.sin(delta_mn)
        )

        Qmn = -(V[m] ** 2 / tap ** 2) * (b + bsh_each) + (V[m] * V[n] / tap) * (
            b * np.cos(delta_mn) - g * np.sin(delta_mn)
        )

        Pnm = (V[n] ** 2) * g - (V[n] * V[m] / tap) * (
            g * np.cos(delta_nm) + b * np.sin(delta_nm)
        )

        Qnm = -(V[n] ** 2) * (b + bsh_each) + (V[n] * V[m] / tap) * (
            b * np.cos(delta_nm) - g * np.sin(delta_nm)
        )

        Smn = np.sqrt(Pmn ** 2 + Qmn ** 2)
        Snm = np.sqrt(Pnm ** 2 + Qnm ** 2)

        carregamento = max(Smn, Snm)

        if carregamento > cap:
            status = "VIOLADO"
        else:
            status = "OK"

        resultados.append({
            "de": barra_m,
            "para": barra_n,
            "ncir": int(circuito["ncir"]),
            "Pkm": Pmn,
            "Qkm": Qmn,
            "Skm": Smn,
            "Pmk": Pnm,
            "Qmk": Qnm,
            "Smk": Snm,
            "Pperdas": Pmn + Pnm,
            "Qperdas": Qmn + Qnm,
            "cap": cap,
            "carregamento": carregamento,
            "uso_%": 100 * carregamento / cap,
            "status": status
        })

    return pd.DataFrame(resultados)