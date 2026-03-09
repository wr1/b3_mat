"""Tests for materials module."""

import json
import os
import tempfile
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from b3_mat.materials import IsotropicMaterial, MaterialDB, OrthotropicMaterial


def test_isotropic_material():
    mat = IsotropicMaterial(E=1e9, nu=0.3, rho=1000, name="test")
    assert mat.E == 1e9
    assert mat.nu == 0.3
    assert mat.rho == 1000
    assert mat.name == "test"


def test_isotropic_material_clamp_nu():
    mat = IsotropicMaterial(E=1e9, nu=0.5, rho=1000)
    assert mat.nu == 0.49


def test_isotropic_material_invalid_nu():
    with pytest.raises(ValidationError):
        IsotropicMaterial(E=1e9, nu=-0.1, rho=1000)


def test_orthotropic_material():
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
        name="test",
    )
    assert mat.Ex == 1e9
    assert mat.Ey == 2e9
    assert mat.Ez == 3e9
    assert mat.Gxy == 1e8
    assert mat.Gxz == 2e8
    assert mat.Gyz == 3e8
    assert mat.nuxy == 0.3
    assert mat.nuxz == 0.2
    assert mat.nuyz == 0.1
    assert mat.rho == 1500
    assert mat.name == "test"


def test_material_db():
    db = MaterialDB()
    db.materials["iso"] = IsotropicMaterial(E=1e9, nu=0.3, rho=1000)
    db.materials["ortho"] = OrthotropicMaterial(
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
    assert len(db.materials) == 2
    assert isinstance(db.get_material("iso"), IsotropicMaterial)
    assert isinstance(db.get_material("ortho"), OrthotropicMaterial)


def test_material_db_get_missing():
    db = MaterialDB()
    with pytest.raises(KeyError):
        db.get_material("missing")


def test_material_db_from_yaml():
    yaml_content = """
iso:
  E: 1000000000
  nu: 0.3
  rho: 1000
ortho:
  Ex: 1000000000
  Ey: 2000000000
  Ez: 3000000000
  Gxy: 100000000
  Gxz: 200000000
  Gyz: 300000000
  nuxy: 0.3
  nuxz: 0.2
  nuyz: 0.1
  rho: 1500
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        f.flush()
        db = MaterialDB.from_yaml(f.name)
    os.unlink(f.name)
    assert "iso" in db.materials
    assert isinstance(db.materials["iso"], IsotropicMaterial)
    assert db.materials["iso"].E == 1e9
    assert "ortho" in db.materials
    assert isinstance(db.materials["ortho"], OrthotropicMaterial)
    assert db.materials["ortho"].Ex == 1e9


def test_material_db_from_yaml_file_not_found():
    with pytest.raises(FileNotFoundError):
        MaterialDB.from_yaml("nonexistent.yaml")


def test_material_db_from_json():
    json_content = {
        "iso": {"E": 1e9, "nu": 0.3, "rho": 1000},
        "ortho": {
            "Ex": 1e9,
            "Ey": 2e9,
            "Ez": 3e9,
            "Gxy": 1e8,
            "Gxz": 2e8,
            "Gyz": 3e8,
            "nuxy": 0.3,
            "nuxz": 0.2,
            "nuyz": 0.1,
            "rho": 1500,
        },
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(json_content, f)
        f.flush()
        db = MaterialDB.from_json(f.name)
    os.unlink(f.name)
    assert "iso" in db.materials
    assert isinstance(db.materials["iso"], IsotropicMaterial)
    assert "ortho" in db.materials
    assert isinstance(db.materials["ortho"], OrthotropicMaterial)


def test_material_db_from_json_file_not_found():
    with pytest.raises(FileNotFoundError):
        MaterialDB.from_json("nonexistent.json")
