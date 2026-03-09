"""Tests for Calculix export."""

import json
import tempfile
import os

from b3_mat.calculix import material_db_to_ccx


def test_material_db_to_ccx():
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
        result = material_db_to_ccx([1, 2], f.name)
    os.unlink(f.name)
    assert "*material,name=m1" in result
    assert "*elastic,type=iso" in result
    assert "*material,name=m2" in result
    assert "*elastic,type=engineering constants" in result


def test_material_db_to_ccx_file_not_found():
    import pytest
    with pytest.raises(FileNotFoundError):
        material_db_to_ccx([1], "nonexistent.json")
