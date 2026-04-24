# Trabalho de SEP2 - Análise de Fluxo de Potência
# Aluno: Vinicius Silvestre 210950064

import pandas as pd

from leitura import ler_dados_sistema
from ybus import montar_ybus
from newtonraphson import fluxo_newton_raphson
from fluxos import calcular_fluxos
from limites import (
    verificar_limites_tensao,
    verificar_limites_geracao,
    verificar_limites_circuitos
)


arquivo = "dados_sistema13B_EC1.txt"

barras, circuitos = ler_dados_sistema(arquivo)

ybus = montar_ybus(barras, circuitos)

V, ang, Pcalc, Qcalc = fluxo_newton_raphson(barras, ybus)

fluxos = calcular_fluxos(barras, circuitos, V, ang)

resultados_barras = barras.copy()

resultados_barras["V(pu)"] = V
resultados_barras["theta(graus)"] = ang
resultados_barras["Pinj(pu)"] = Pcalc
resultados_barras["Qinj(pu)"] = Qcalc
resultados_barras["Pg(pu)"] = Pcalc + resultados_barras["PD"]
resultados_barras["Qg(pu)"] = Qcalc + resultados_barras["QD"]

limites_tensao = verificar_limites_tensao(barras, V)
limites_geracao = verificar_limites_geracao(barras, Pcalc)
limites_circuitos = verificar_limites_circuitos(fluxos)


print("\n=========== RESULTADOS DAS BARRAS ===========\n")

print(
    resultados_barras[
        [
            "barra",
            "tipo",
            "V(pu)",
            "theta(graus)",
            "Pinj(pu)",
            "Qinj(pu)",
            "Pg(pu)",
            "Qg(pu)"
        ]
    ].round(4).to_string(index=False)
)


print("\n=========== FLUXOS NOS CIRCUITOS ===========\n")

print(
    fluxos[
        [
            "de",
            "para",
            "ncir",
            "Pkm",
            "Qkm",
            "Skm",
            "Pmk",
            "Qmk",
            "Smk",
            "Pperdas",
            "Qperdas",
            "cap",
            "status"
        ]
    ].round(4).to_string(index=False)
)


print("\n=========== LIMITES DE TENSÃO ===========\n")

print(
    limites_tensao.round(4).to_string(index=False)
)


print("\n=========== LIMITES DE GERAÇÃO ATIVA ===========\n")

print(
    limites_geracao.round(4).to_string(index=False)
)


print("\n=========== LIMITES DOS CIRCUITOS ===========\n")

print(
    limites_circuitos.round(4).to_string(index=False)
)