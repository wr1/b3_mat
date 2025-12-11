"""Export materials to ANBA format."""
from __future__ import annotations

import json
import logging
import os

import numpy as np
from anba4 import material as anba_material

logger = logging.getLogger(__name__)


def get_material_db_anba(
    material_map: str, unit_factor: float = 1.0
) -> dict[str, anba_material.Material]:
    """Load and process material database for ANBA from JSON material map."""
    if not os.path.isfile(material_map):
        msg = f"Material map file not found: {material_map}"
        raise FileNotFoundError(msg)

    with open(material_map) as f:
        mm1 = json.load(f)
        mm = mm1.get("map", mm1)
        mat_db_data = mm1.get("matdb", None)

    if "-1" in mat_db_data:
        mm["-1"] = -1

    materials = {}
    for mat_name in mm:
        if mat_name == "matdb":
            continue
        matdb_id = mat_name
        if matdb_id not in mat_db_data:
            logger.error(f"Material ID {matdb_id} not found in materials.yaml")
            msg = f"Material ID {matdb_id} not found"
            raise KeyError(msg)
        matdb_entry = mat_db_data[matdb_id]
        logger.debug(f"Processing material {matdb_id}: {matdb_entry}")
        density = matdb_entry.get("rho", matdb_entry.get("density", 1.0))

        if "Ex" in matdb_entry and "Ey" in matdb_entry and "Ez" in matdb_entry:
            required_keys = [
                "Ex",
                "Ey",
                "Ez",
                "Gxy",
                "Gxz",
                "Gyz",
                "nuxy",
                "nuxz",
                "nuyz",
            ]
            if not all(k in matdb_entry for k in required_keys):
                msg = f"Missing orthotropic properties for {matdb_id}"
                raise ValueError(msg)
            matMechanicProp = np.zeros((3, 3))
            matMechanicProp[0, 2] = matdb_entry["Ex"] * unit_factor
            matMechanicProp[0, 1] = matdb_entry["Ey"] * unit_factor
            matMechanicProp[0, 0] = matdb_entry["Ez"] * unit_factor
            matMechanicProp[1, 2] = matdb_entry["Gyz"] * unit_factor
            matMechanicProp[1, 1] = matdb_entry["Gxz"] * unit_factor
            matMechanicProp[1, 0] = matdb_entry["Gxy"] * unit_factor
            matMechanicProp[2, 2] = matdb_entry["nuyz"]
            matMechanicProp[2, 1] = matdb_entry["nuxz"]
            matMechanicProp[2, 0] = matdb_entry["nuxy"]
            materials[matdb_id] = anba_material.OrthotropicMaterial(
                matMechanicProp, density
            )
        else:
            if "E" not in matdb_entry and "Ex" not in matdb_entry:
                msg = f"Missing 'E' or 'Ex' for isotropic {matdb_id}"
                raise ValueError(msg)
            E = matdb_entry.get("E", matdb_entry.get("Ex")) * unit_factor
            nu = min(matdb_entry["nu"], 0.49)
            materials[matdb_id] = anba_material.IsotropicMaterial([E, nu], density)

    return materials


# Note: Additional ANBA-specific functions like solve_anba4 can be added here if needed.
