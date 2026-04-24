import numpy as np


def fluxo_newton_raphson(barras, ybus, tol=1e-6, max_iter=30):
    nb = len(barras)

    tipos = barras["tipo"].values

    V = barras["Vesp"].values.astype(float)
    theta = np.radians(barras["Oesp"].values.astype(float))

    Pg = barras["PGesp"].values.astype(float)
    Pd = barras["PD"].values.astype(float)
    Qd = barras["QD"].values.astype(float)

    Pesp = Pg - Pd
    Qesp = -Qd

    pq = [i for i in range(nb) if tipos[i] == "PQ"]
    pv = [i for i in range(nb) if tipos[i] == "PV"]
    sw = [i for i in range(nb) if tipos[i] == "SW"]

    pvpq = pv + pq

    G = ybus.real
    B = ybus.imag

    for it in range(max_iter):

        Pcalc = np.zeros(nb)
        Qcalc = np.zeros(nb)

        for i in range(nb):
            for k in range(nb):
                ang = theta[i] - theta[k]
                Pcalc[i] += V[i] * V[k] * (G[i, k] * np.cos(ang) + B[i, k] * np.sin(ang))
                Qcalc[i] += V[i] * V[k] * (G[i, k] * np.sin(ang) - B[i, k] * np.cos(ang))

        dP = Pesp - Pcalc
        dQ = Qesp - Qcalc

        mismatch = np.concatenate([dP[pvpq], dQ[pq]])

        if np.max(np.abs(mismatch)) < tol:
            print(f"Convergiu em {it+1} iterações.")
            break

        npv_pq = len(pvpq)
        npq = len(pq)

        H = np.zeros((npv_pq, npv_pq))
        N = np.zeros((npv_pq, npq))
        M = np.zeros((npq, npv_pq))
        L = np.zeros((npq, npq))

        for a, i in enumerate(pvpq):
            for b, k in enumerate(pvpq):
                if i == k:
                    H[a, b] = -Qcalc[i] - B[i, i] * V[i] ** 2
                else:
                    ang = theta[i] - theta[k]
                    H[a, b] = V[i] * V[k] * (G[i, k] * np.sin(ang) - B[i, k] * np.cos(ang))

        for a, i in enumerate(pvpq):
            for b, k in enumerate(pq):
                if i == k:
                    N[a, b] = Pcalc[i] / V[i] + G[i, i] * V[i]
                else:
                    ang = theta[i] - theta[k]
                    N[a, b] = V[i] * (G[i, k] * np.cos(ang) + B[i, k] * np.sin(ang))

        for a, i in enumerate(pq):
            for b, k in enumerate(pvpq):
                if i == k:
                    M[a, b] = Pcalc[i] - G[i, i] * V[i] ** 2
                else:
                    ang = theta[i] - theta[k]
                    M[a, b] = -V[i] * V[k] * (G[i, k] * np.cos(ang) + B[i, k] * np.sin(ang))

        for a, i in enumerate(pq):
            for b, k in enumerate(pq):
                if i == k:
                    L[a, b] = Qcalc[i] / V[i] - B[i, i] * V[i]
                else:
                    ang = theta[i] - theta[k]
                    L[a, b] = V[i] * (G[i, k] * np.sin(ang) - B[i, k] * np.cos(ang))

        J = np.block([[H, N],
                      [M, L]])

        dx = np.linalg.solve(J, mismatch)

        dtheta = dx[:npv_pq]
        dV = dx[npv_pq:]

        for a, i in enumerate(pvpq):
            theta[i] += dtheta[a]

        for a, i in enumerate(pq):
            V[i] += dV[a]

    return V, np.degrees(theta), Pcalc, Qcalc