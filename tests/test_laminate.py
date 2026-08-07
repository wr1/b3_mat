"""Tests for laminate module (pure CLT — no lamprop/composipy)."""

import numpy as np

from b3_mat.laminate import Laminate, calculate_laminate_properties
from b3_mat.materials import OrthotropicMaterial


def _mat() -> OrthotropicMaterial:
    return OrthotropicMaterial(
        Ex=1e9,
        Ey=2e9,
        Ez=3e9,
        Gxy=1e8,
        Gxz=2e8,
        Gyz=3e8,
        nuxy=0.3,
        nuxz=0.2,
        nuyz=0.1,
        rho=1500,
    )


def test_laminate_calculation():
    layers = [(_mat(), 0.001, 0), (_mat(), 0.001, 90)]
    props = calculate_laminate_properties(layers)
    assert "A" in props and "B" in props and "D" in props and "ABD" in props
    assert props["thickness"] == 0.002
    assert props["Ex"] > 0 and props["Ey"] > 0


def test_laminate_matrices():
    lam = Laminate([(_mat(), 0.125e-3, 0), (_mat(), 0.125e-3, 90)])
    assert lam.A.shape == (3, 3)
    assert lam.ABD.shape == (6, 6)
    np.testing.assert_allclose(lam.A, lam.A.T)
