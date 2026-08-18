"""
Tests automatisés — exécutés par la CI à chaque commit.

Montre que tu sais tester ton automatisation, pas juste l'écrire.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from validate import check_device, load_inventory  # noqa: E402


@pytest.fixture
def devices():
    return load_inventory()


def test_inventory_not_empty(devices):
    assert len(devices) > 0, "L'inventaire ne doit pas être vide"


def test_all_devices_are_compliant(devices):
    """Chaque équipement de l'inventaire doit passer les règles de conformité."""
    for device in devices:
        errors = check_device(device)
        assert not errors, f"{device['hostname']} non conforme : {errors}"


def test_hostnames_are_unique(devices):
    names = [d["hostname"] for d in devices]
    assert len(names) == len(set(names)), "Des hostnames sont dupliqués"


def test_mgmt_ips_are_unique(devices):
    ips = [d["mgmt_ip"] for d in devices]
    assert len(ips) == len(set(ips)), "Des IP de management sont dupliquées"


def test_non_compliant_device_is_caught():
    """Sanity check : un équipement volontairement cassé doit être rejeté."""
    bad = {"hostname": "switch1", "vlans": [], "ntp_servers": [], "mgmt_ip": ""}
    assert check_device(bad), "Un équipement non conforme aurait dû lever des erreurs"
