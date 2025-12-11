"""Command-line interface for b3_mat."""

import argparse
import sys

from .materials import MaterialDB


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="b3_mat CLI")
    parser.add_argument(
        "-f", "--file", required=True, help="Path to material file (YAML or JSON)"
    )
    parser.add_argument("-o", "--output", help="Output format: calculix or anba")
    parser.add_argument("-m", "--matmap", help="Material map JSON for export")
    args = parser.parse_args()

    if args.file.endswith(".yml") or args.file.endswith(".yaml"):
        MaterialDB.from_yaml(args.file)
    elif args.file.endswith(".json"):
        MaterialDB.from_json(args.file)
    else:
        sys.exit(1)

    if args.output == "calculix":
        from .calculix import material_db_to_ccx

        # Assuming materials list is needed; for demo, use dummy
        materials = [1.0]  # Placeholder
        material_db_to_ccx(materials, args.matmap)
    elif args.output == "anba":
        from .anba import get_material_db_anba

        get_material_db_anba(args.matmap)
    else:
        pass


if __name__ == "__main__":
    main()
