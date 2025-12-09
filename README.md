# b3_mat

A library for handling composite material data in b3m, tying together material data across various contexts like 3D FEA (Calculix, ANSYS), classical laminate theory calculations, 2D FEA (ANBA, BECAS), fatigue damage, and material volume/mass/cost.

## Features

- Material data models using Pydantic for validation and serialization.
- Support for isotropic and orthotropic materials.
- Exporters for ANBA and Calculix formats.
- Integration with composipy and lamprop for laminate calculations.
- CLI for material processing and export.

## Installation

```bash
pip install -e .
```

## Usage

### CLI

```bash
b3_mat --help
```

### Python API

```python
from b3_mat import MaterialDB

# Load materials from YAML
mat_db = MaterialDB.from_yaml("materials_si.yml")

# Export to Calculix format
ccx_block = mat_db.to_calculix()
print(ccx_block)
```

## Development

Run tests:

```bash
pytest
```

Format and lint:

```bash
ruff format
ruff check --fix
```