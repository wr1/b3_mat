"""Export materials to Calculix format."""

import json
import logging
import os
from typing import List

import numpy as np

logger = logging.getLogger(__name__)


def material_db_to_ccx(
    materials: List[float], matmap: str, force_iso: bool = False
) -> str:
    """Generate Calculix material block from material map."""
    if not os.path.isfile(matmap):
        raise FileNotFoundError("No material map defined")

    with open(matmap) as f:
        mm1 = json.load(f)
        mm = mm1["map"]
        mat_db = mm1["matdb"]

    mm_inv = {v: k for k, v in mm.items()}

    matblock = ""
    for i in materials:
        if i > 1e-6:
            material_properties = mat_db[mm_inv[int(i)]]
            matblock += (
                f"** material: {mm_inv[int(i)]} {i} {material_properties['name']}\n"
            )

            if "C" in material_properties and not force_iso:
                logger.info(f"{material_properties['name']} is orthotropic")
                C = np.array(material_properties["C"])
                matblock += "** orthotropic material\n"
                matblock += f"*material,name=m{int(i)}\n*elastic,type=ortho\n"
                D = C.copy()
                D[0, 3] = C[0, 5]
                D[0, 5] = C[0, 3]
                D[1, 3] = C[1, 5]
                D[1, 5] = C[1, 3]
                D[2, 3] = C[2, 5]
                D[2, 5] = C[2, 3]
                D[3, 3] = C[5, 5]
                D[5, 5] = C[3, 3]
                matblock += (
                    f"{D[0, 0]:.4g},{D[0, 1]:.4g},{D[1, 1]:.4g},"
                    f"{D[0, 2]:.4g},{D[1, 2]:.4g},{D[2, 2]:.4g},"
                    f"{D[3, 3]:.4g},{D[4, 4]:.4g},\n"
                    f"{D[5, 5]:.4g},293\n"
                )
            elif "Ex" in material_properties and not force_iso:
                logger.info(f"{material_properties['name']} has engineering constants")
                matblock += "** orthotropic material\n"
                matblock += (
                    f"*material,name=m{int(i)}\n*elastic,type=engineering constants\n"
                )
                matblock += (
                    f"{material_properties['Ex']:.4g},{material_properties['Ey']:.4g},{material_properties['Ez']:.4g},"
                    f"{material_properties['nuxy']:.4g},{material_properties['nuxz']:.4g},{material_properties['nuyz']:.4g},"
                    f"{material_properties['Gxy']:.4g},{material_properties['Gxz']:.4g},\n"
                    f"{material_properties['Gyz']:.4g},293\n"
                )
            else:
                logger.info(f"{material_properties['name']} is isotropic")
                nu = min(
                    0.45,
                    max(
                        0.1,
                        material_properties.get(
                            "nu", material_properties.get("nuxy", 0.3)
                        ),
                    ),
                )
                E = material_properties.get("Ex", material_properties.get("E", 1e9))
                matblock += "** isotropic material\n"
                matblock += f"*material,name=m{int(i)}\n*elastic,type=iso\n"
                matblock += f"{E:.4g},{nu:.4g},293\n"

    return matblock
