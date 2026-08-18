#!/usr/bin/env python3
"""
Contrôle de conformité (compliance) des équipements.

En NetDevOps, on ne se contente pas de générer : on VALIDE que
chaque config respecte les standards de l'entreprise AVANT tout
déploiement. Ces règles sont volontairement simples mais réalistes.

Règles vérifiées :
  1. Le hostname suit la convention  sw-<site>-<role>-NN
  2. Le VLAN de management (99) est présent partout
  3. Au moins 2 serveurs NTP  (redondance temporelle = obligatoire)
  4. Une IP de management est définie
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
HOSTNAME_RE = re.compile(r"^sw-(par|tls)-(access|core)-\d{2}$")
MGMT_VLAN_ID = 99


def load_inventory() -> list[dict]:
    with open(ROOT / "inventory" / "devices.yml") as f:
        return yaml.safe_load(f)["devices"]


def check_device(device: dict) -> list[str]:
    """Retourne la liste des violations pour un équipement (vide = conforme)."""
    errors: list[str] = []
    name = device.get("hostname", "<sans nom>")

    if not HOSTNAME_RE.match(name):
        errors.append(f"hostname '{name}' ne respecte pas la convention sw-<site>-<role>-NN")

    vlan_ids = {v["id"] for v in device.get("vlans", [])}
    if MGMT_VLAN_ID not in vlan_ids:
        errors.append(f"VLAN de management {MGMT_VLAN_ID} absent")

    ntp = device.get("ntp_servers", [])
    if len(ntp) < 2:
        errors.append(f"redondance NTP insuffisante ({len(ntp)} serveur(s), 2 minimum)")

    if not device.get("mgmt_ip"):
        errors.append("IP de management manquante")

    return errors


def main() -> None:
    devices = load_inventory()
    total_errors = 0

    print("Contrôle de conformité...")
    for device in devices:
        name = device.get("hostname", "<sans nom>")
        errors = check_device(device)
        if errors:
            total_errors += len(errors)
            print(f"  ✗ {name}")
            for e in errors:
                print(f"      - {e}")
        else:
            print(f"  ✓ {name} — conforme")

    if total_errors:
        print(f"\n{total_errors} violation(s) détectée(s) — déploiement bloqué.")
        sys.exit(1)  # code de sortie != 0 => la CI échoue
    print("\nTous les équipements sont conformes.")


if __name__ == "__main__":
    main()
