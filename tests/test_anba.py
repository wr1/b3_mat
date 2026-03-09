"""Tests for ANBA export."""

import json
import tempfile
import os
import pytest

anba4 = pytest.importorskip("anba4")

from b3_mat.anba import get_material_db_anba


def test_get_material_db_anba():
    matmap_data = {
        "map": {"mat1": 1, "mat2": 2},
        "matdb": {
            "mat1": {"name": "iso", "E": 1e9, "nu": 0.3, "rho": 1000},
            "mat2": {
                "name": "ortho",
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
        },
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(matmap_data, f)
        f.flush()
        materials = get_material_db_anba(f.name)
    os.unlink(f.name)
    assert "mat1" in materials
    assert "mat2" in materials
    assert isinstance(materials["mat1"], anba4.material.IsotropicMaterial)
    assert isinstance(materials["mat2"], anba4.material.OrthotropicMaterial)


def test_get_material_db_anba_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_material_db_anba("nonexistent.json")
