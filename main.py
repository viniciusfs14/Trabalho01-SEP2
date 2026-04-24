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

limites_tensao = verificar_limites_tensao(barras, V)
limites_geracao = verificar_limites_geracao(barras, Pcalc)
limites_circuitos = verificar_limites_circuitos(fluxos)

print("\n=========== LIMITES DE TENSÃO ===========\n")
print(limites_tensao.round(4))

print("\n=========== LIMITES DE GERAÇÃO ATIVA ===========\n")
print(limites_geracao.round(4))

print("\n=========== LIMITES DOS CIRCUITOS ===========\n")
print(limites_circuitos.round(4))