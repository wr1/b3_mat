"""b3_mat: Library for composite material data handling."""

from .laminate import calculate_laminate_properties
from .materials import IsotropicMaterial, MaterialDB, OrthotropicMaterial

__all__ = [
    "IsotropicMaterial",
    "MaterialDB",
    "OrthotropicMaterial",
    "calculate_laminate_properties",
]
