"""Tests for laminate module."""

from b3_mat.laminate import calculate_laminate_properties
from b3_mat.materials import OrthotropicMaterial


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
    assert props["thickness"] == 0.002
