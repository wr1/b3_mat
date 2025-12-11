"""Material data models using Pydantic."""
from __future__ import annotations

import json
import os
from typing import Union

import yaml
from pydantic import BaseModel, Field, validator


class IsotropicMaterial(BaseModel):
    """Isotropic material model."""

    E: float = Field(..., description="Young's modulus")
    nu: float = Field(..., ge=0, le=0.49, description="Poisson's ratio")
    rho: float = Field(..., gt=0, description="Density")
    name: str | None = None

    @validator("nu", pre=True, always=True)
    def clamp_nu(self, v):
        return min(v, 0.49)


class OrthotropicMaterial(BaseModel):
    """Orthotropic material model."""

    Ex: float = Field(..., gt=0, description="Young's modulus in x")
    Ey: float = Field(..., gt=0, description="Young's modulus in y")
    Ez: float = Field(..., gt=0, description="Young's modulus in z")
    Gxy: float = Field(..., gt=0, description="Shear modulus xy")
    Gxz: float = Field(..., gt=0, description="Shear modulus xz")
    Gyz: float = Field(..., gt=0, description="Shear modulus yz")
    nuxy: float = Field(..., description="Poisson's ratio xy")
    nuxz: float = Field(..., description="Poisson's ratio xz")
    nuyz: float = Field(..., description="Poisson's ratio yz")
    rho: float = Field(..., gt=0, description="Density")
    name: str | None = None


Material = Union[IsotropicMaterial, OrthotropicMaterial]


class MaterialDB(BaseModel):
    """Database of materials."""

    materials: dict[str, Material] = Field(default_factory=dict)

    @classmethod
    def from_yaml(cls, filepath: str) -> MaterialDB:
        """Load materials from YAML file."""
        if not os.path.isfile(filepath):
            msg = f"File not found: {filepath}"
            raise FileNotFoundError(msg)
        with open(filepath) as f:
            data = yaml.safe_load(f)
        materials = {}
        for key, props in data.items():
            if "Ex" in props and "Ey" in props and "Ez" in props:
                materials[key] = OrthotropicMaterial(**props)
            else:
                materials[key] = IsotropicMaterial(**props)
        return cls(materials=materials)

    @classmethod
    def from_json(cls, filepath: str) -> MaterialDB:
        """Load materials from JSON file."""
        if not os.path.isfile(filepath):
            msg = f"File not found: {filepath}"
            raise FileNotFoundError(msg)
        with open(filepath) as f:
            data = json.load(f)
        materials = {}
        for key, props in data.items():
            if "Ex" in props and "Ey" in props and "Ez" in props:
                materials[key] = OrthotropicMaterial(**props)
            else:
                materials[key] = IsotropicMaterial(**props)
        return cls(materials=materials)

    def get_material(self, key: str) -> Material:
        """Retrieve a material by key."""
        return self.materials[key]
