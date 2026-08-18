# NetDevOps Sandbox — Config-as-Code

Mini-pipeline qui reproduit la **boucle NetDevOps de bout en bout**, sans
matériel réseau : une source de vérité décrit le réseau, un template génère
les configs, un contrôle de conformité les valide, et une CI enchaîne le tout
à chaque commit.

Construit avec des technos que je maîtrise déjà : **Python, Jinja2, YAML,
Git, GitHub Actions, Docker** — plus un bonus **Ansible**.

---

## La boucle reproduite

```
inventory/devices.yml   ->   templates/switch.j2   ->   build/*.cfg   ->   validate.py
   (source de vérité)          (templating Jinja2)      (configs générées)   (conformité)
                                                                                  |
                        tout est enchaîné à chaque push par  .github/workflows/ci.yml
```

| Fichier | Rôle | Concept NetDevOps |
|---|---|---|
| `inventory/devices.yml` | décrit tous les équipements | **source of truth** |
| `templates/switch.j2` | modèle de config | **templating / DRY** |
| `generate.py` | rend une config par équipement | **génération idempotente** |
| `validate.py` | vérifie les standards | **compliance / guardrails** |
| `tests/test_configs.py` | tests automatisés | **shift-left testing** |
| `.github/workflows/ci.yml` | build + validate + test à chaque push | **CI/CD** |
| `Dockerfile` | outil conteneurisé | **reproductibilité** |
| `ansible/playbook.yml` | même logique via Ansible | **outil réseau réel** |

---

## Prérequis

- Python 3.10+
- (bonus) Docker
- (bonus) Ansible : `pip install ansible`

## Lancer le projet (3 minutes)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

python generate.py               # 1. génère les configs dans build/
python validate.py               # 2. contrôle de conformité
pytest -v                        # 3. tests automatisés
```

### Voir les garde-fous en action

Casse un équipement dans `inventory/devices.yml` (ex : renomme un hostname
en `CORE1`, ou retire un serveur NTP) puis relance `python validate.py` :
le contrôle échoue avec un **code de sortie 1** — en CI, le changement serait
bloqué. C'est tout l'intérêt du NetDevOps : on attrape l'erreur AVANT le réseau.

### Bonus Docker

```bash
docker build -t netdevops-sandbox .
docker run --rm netdevops-sandbox
```

### Bonus Ansible

```bash
cd ansible
ansible-playbook -i localhost, playbook.yml   # configs dans build_ansible/
```

Même démarche que `generate.py`. Pour passer à du vrai matériel, on remplace
le module `template` par `cisco.ios.ios_config` — le reste ne bouge pas.

---

## Ce que ce projet démontre (à dire en entretien)

1. **Je connais déjà la mécanique DevOps** que le poste veut appliquer au
   réseau : versioning Git, templating, tests, CI/CD.
2. **Idempotence** : relancer la génération produit le même résultat, jamais
   d'effet de bord — notion centrale en automatisation.
3. **Source of truth** : on ne configure plus équipement par équipement, on
   décrit l'intention une fois et l'outillage s'occupe du reste.
4. **Compliance as code** : les standards (naming, redondance NTP, VLAN mgmt)
   sont vérifiés automatiquement, pas à l'œil.
5. **Je monte vite** : je l'ai construit en une soirée pour cet entretien, et
   je sais quelle brique remplacer (Ansible + modules constructeur) pour le
   brancher sur du vrai réseau.
