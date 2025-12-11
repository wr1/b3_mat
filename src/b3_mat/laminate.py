"""Laminate theory calculations using lamprop."""
from __future__ import annotations

from typing import TYPE_CHECKING

from lamprop import Laminate

if TYPE_CHECKING:
    from .materials import OrthotropicMaterial


def calculate_laminate_properties(
    layers: list[tuple[OrthotropicMaterial, float, float]],
) -> dict:
    """Calculate laminate properties using lamprop.

    Args:
        layers: List of (material, thickness, angle) tuples.

    Returns:
        Dict with A, B, D matrices and other properties.
    """
    lam = Laminate()
    for mat, t, angle in layers:
        lam.add_layer(
            E1=mat.Ex, E2=mat.Ey, v12=mat.nuxy, G12=mat.Gxy, thickness=t, angle=angle
        )
    return {
        "A": lam.A,
        "B": lam.B,
        "D": lam.D,
        "ABD": lam.ABD,
        "thickness": lam.thickness,
        "Ex": lam.Ex,
        "Ey": lam.Ey,
        "Gxy": lam.Gxy,
        "nuxy": lam.vxy,
    }
