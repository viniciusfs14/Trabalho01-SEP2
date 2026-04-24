import numpy as np


def montar_ybus(barras, circuitos):
    nb = len(barras)
    ybus = np.zeros((nb, nb), dtype=complex)

    mapa_barras = {
        int(barra): idx for idx, barra in enumerate(barras["barra"])
    }

    for _, circuito in circuitos.iterrows():
        if circuito["estado"] != "L":
            continue

        k = mapa_barras[int(circuito["de"])]
        m = mapa_barras[int(circuito["para"])]

        r = circuito["r"]
        x = circuito["x"]
        bsh = circuito["bsh"]
        tap = circuito["tap"]
        defasagem = np.deg2rad(circuito["defasagem"])

        z = complex(r, x)
        y = 1 / z

        tap_complexo = tap * np.exp(1j * defasagem)

        ybus[k, k] += (y + 1j * bsh / 2) / (tap_complexo * np.conj(tap_complexo))
        ybus[m, m] += y + 1j * bsh / 2

        ybus[k, m] += -y / np.conj(tap_complexo)
        ybus[m, k] += -y / tap_complexo

    for _, barra in barras.iterrows():
        idx = mapa_barras[int(barra["barra"])]
        ybus[idx, idx] += 1j * barra["Bsh"]

    return ybus