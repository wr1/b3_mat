"""Tests for materials module."""

import pytest
from b3_mat.materials import IsotropicMaterial, OrthotropicMaterial, MaterialDB


def test_isotropic_material():
    mat = IsotropicMaterial(E=1e9, nu=0.3, rho=1000, name="test")
    assert mat.E == 1e9
    assert mat.nu == 0.3


def test_orthotropic_material():
    mat = OrthotropicMaterial(
        Ex=1e9, Ey=2e9, Ez=3e9,
        Gxy=1e8, Gxz=2e8, Gyz=3e8,
        nuxy=0.3, nuxz=0.2, nuyz=0.1,
        rho=1500, name="test"
    )
    assert mat.Ex == 1e9


def test_material_db():
    db = MaterialDB()
    db.materials["iso"] = IsotropicMaterial(E=1e9, nu=0.3, rho=1000)
    assert len(db.materials) == 1