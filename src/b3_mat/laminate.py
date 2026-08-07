"""Classical Laminate Theory (CLT) calculations."""

from __future__ import annotations

import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .materials import OrthotropicMaterial


class Laminate:
    """Laminate class implementing Classical Laminate Theory."""

    def __init__(self, layers: list[tuple[OrthotropicMaterial, float, float]]):
        """layers: list of (OrthotropicMaterial, thickness, angle_deg)."""
        self.layers = layers
        self._z = None
        self._A = None
        self._B = None
        self._D = None
        self._ABD = None
        self._compute_z_positions()
        self._compute_abd()

    def _compute_z_positions(self):
        total_thickness = sum(t for _, t, _ in self.layers)
        z = np.cumsum([0.0] + [t for _, t, _ in self.layers])
        self._z = z - total_thickness / 2

    def _reduced_stiffness(self, mat: OrthotropicMaterial) -> np.ndarray:
        """Q matrix in principal material coordinates."""
        nu21 = mat.nuxy * mat.Ey / mat.Ex
        denom = 1 - mat.nuxy * nu21
        Q11 = mat.Ex / denom
        Q22 = mat.Ey / denom
        Q12 = mat.nuxy * mat.Ey / denom
        Q66 = mat.Gxy
        return np.array([[Q11, Q12, 0], [Q12, Q22, 0], [0, 0, Q66]])

    def _transformed_stiffness(self, Q: np.ndarray, theta: float) -> np.ndarray:
        """Transformed Qbar matrix for given angle (deg)."""
        th = np.deg2rad(theta)
        m, n = np.cos(th), np.sin(th)
        # Compute powers sequentially to avoid UnboundLocalError
        m2 = m**2
        n2 = n**2
        m4 = m**4
        n4 = n**4
        mn2 = m2 * n2

        Q11, Q12, Q22, Q66 = Q[0, 0], Q[0, 1], Q[1, 1], Q[2, 2]

        Qbar11 = Q11 * m4 + Q22 * n4 + 2 * (Q12 + 2 * Q66) * mn2
        Qbar22 = Q11 * n4 + Q22 * m4 + 2 * (Q12 + 2 * Q66) * mn2
        Qbar12 = (Q11 + Q22 - 4 * Q66) * mn2 + Q12 * (m4 + n4)
        Qbar66 = (Q11 + Q22 - 2 * Q12 - 2 * Q66) * mn2 + Q66 * (m4 + n4)
        Qbar16 = (Q11 - Q12 - 2 * Q66) * m**3 * n - (Q22 - Q12 - 2 * Q66) * m * n**3
        Qbar26 = (Q11 - Q12 - 2 * Q66) * m * n**3 - (Q22 - Q12 - 2 * Q66) * m**3 * n

        return np.array([
            [Qbar11, Qbar12, Qbar16],
            [Qbar12, Qbar22, Qbar26],
            [Qbar16, Qbar26, Qbar66]
        ])

    def _compute_abd(self):
        """Compute ABD stiffness matrices."""
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        D = np.zeros((3, 3))

        for i, (mat, tk, angle) in enumerate(self.layers):
            Q = self._reduced_stiffness(mat)
            Qbar = self._transformed_stiffness(Q, angle)
            z1, z2 = self._z[i], self._z[i + 1]
            A += Qbar * (z2 - z1)
            B += Qbar * 0.5 * (z2**2 - z1**2)
            D += Qbar * (z2**3 - z1**3) / 3

        self._A = A
        self._B = B
        self._D = D
        self._ABD = np.block([[A, B], [B, D]])

    @property
    def A(self) -> np.ndarray:
        return self._A

    @property
    def B(self) -> np.ndarray:
        return self._B

    @property
    def D(self) -> np.ndarray:
        return self._D

    @property
    def ABD(self) -> np.ndarray:
        return self._ABD

    @property
    def total_thickness(self) -> float:
        return self._z[-1] - self._z[0]

    def engineering_properties(self) -> dict:
        """In-plane engineering constants (from A matrix)."""
        a = np.linalg.inv(self.A)
        h = self.total_thickness
        Ex = 1 / (a[0, 0] * h)
        Ey = 1 / (a[1, 1] * h)
        Gxy = 1 / (a[2, 2] * h)
        nuxy = -a[0, 1] / a[0, 0]
        return {
            "Ex": Ex,
            "Ey": Ey,
            "Gxy": Gxy,
            "nuxy": nuxy,
            "thickness": h,
        }


def calculate_laminate_properties(
    layers: list[tuple[OrthotropicMaterial, float, float]],
) -> dict:
    """Calculate laminate properties using CLT (backward compatible)."""
    lam = Laminate(layers)
    props = lam.engineering_properties()
    props.update({
        "A": lam.A,
        "B": lam.B,
        "D": lam.D,
        "ABD": lam.ABD,
    })
    return props
