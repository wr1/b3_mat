"""b3_mat: Library for composite material data handling."""

from .laminate import Laminate, calculate_laminate_properties
from .materials import IsotropicMaterial, MaterialDB, OrthotropicMaterial

__all__ = [
    "IsotropicMaterial",
    "MaterialDB",
    "OrthotropicMaterial",
    "Laminate",
    "calculate_laminate_properties",
]
