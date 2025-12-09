"""b3_mat: Library for composite material data handling."""

from .materials import IsotropicMaterial, OrthotropicMaterial, MaterialDB
from .laminate import calculate_laminate_properties

__all__ = [
    "IsotropicMaterial",
    "OrthotropicMaterial",
    "MaterialDB",
    "calculate_laminate_properties",
]