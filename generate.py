#!/usr/bin/env python3
"""
Génère une config par équipement à partir de :
  - la source de vérité  (inventory/devices.yml)
  - un template Jinja2    (templates/switch.j2)

Point clé pour l'entretien : ce script est IDEMPOTENT.
Le lancer 2 fois produit exactement les mêmes fichiers.
"""
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent
BUILD_DIR = ROOT / "build"


def load_inventory() -> list[dict]:
    with open(ROOT / "inventory" / "devices.yml") as f:
        return yaml.safe_load(f)["devices"]


def render_configs(devices: list[dict]) -> None:
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("switch.j2")

    BUILD_DIR.mkdir(exist_ok=True)
    for device in devices:
        config = template.render(device=device)
        out_file = BUILD_DIR / f"{device['hostname']}.cfg"
        out_file.write_text(config)
        print(f"  ✓ généré : {out_file.relative_to(ROOT)}")


def main() -> None:
    devices = load_inventory()
    print(f"Génération des configs pour {len(devices)} équipement(s)...")
    render_configs(devices)
    print("Terminé.")


if __name__ == "__main__":
    main()
