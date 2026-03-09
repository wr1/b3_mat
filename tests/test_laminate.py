"""Tests for laminate module."""

import numpy as np
import pytest

from b3_mat.laminate import Laminate, calculate_laminate_properties
from b3_mat.materials import OrthotropicMaterial

composipy = pytest.importorskip("composipy")


def test_laminate_calculation():
    mat = OrthotropicMaterial(
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
    layers = [(mat, 0.001, 0), (mat, 0.001, 90)]
    props = calculate_laminate_properties(layers)
    assert "A" in props
    assert "B" in props
    assert "D" in props
    assert "ABD" in props
    assert props["thickness"] == 0.002
    assert "Ex" in props
    assert "Ey" in props
    assert "Gxy" in props
    assert "nuxy" in props


def test_laminate_properties():
    mat = OrthotropicMaterial(
        Ex=150e9,
        Ey=10e9,
        Ez=10e9,
        Gxy=5e9,
        Gxz=5e9,
        Gyz=3.5e9,
        nuxy=0.3,
        nuxz=0.3,
        nuyz=0.4,
        rho=1600,
    )
    layers = [
        (mat, 0.125e-3, 0),
        (mat, 0.125e-3, 90),
        (mat, 0.125e-3, 90),
        (mat, 0.125e-3, 0),
    ]
    lam = Laminate(layers)
    eng = lam.engineering_properties()
    assert eng["thickness"] == 0.5e-3
    assert eng["Ex"] > 0
    assert eng["Ey"] > 0
    assert eng["Gxy"] > 0
    assert abs(eng["nuxy"]) < 1

    # Check matrices shapes
    assert lam.A.shape == (3, 3)
    assert lam.B.shape == (3, 3)
    assert lam.D.shape == (3, 3)
    assert lam.ABD.shape == (6, 6)

    # Check symmetry
    np.testing.assert_allclose(lam.A, lam.A.T)
    np.testing.assert_allclose(lam.D, lam.D.T)
