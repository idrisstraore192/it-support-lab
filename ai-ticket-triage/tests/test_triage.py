import sys, csv
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import triage

KB = triage.load_kb()
def t(sujet, desc): return {"id": "X", "sujet": sujet, "description": desc}

def test_password():
    r = triage.triage_ticket(t("Connexion", "mon mot de passe ne fonctionne plus, compte verrouillé"), KB)
    assert r["categorie"] == "Compte et accès"

def test_phishing_is_security_and_escalated():
    r = triage.triage_ticket(t("Courriel", "lien suspect, j'ai peut-être cliqué, phishing"), KB)
    assert r["categorie"] == "Sécurité" and r["escalade"] == "Oui"

def test_urgent():
    r = triage.triage_ticket(t("URGENT", "tout le service est bloqué, production arrêtée, réseau"), KB)
    assert r["priorite"].startswith("P1")

def test_unknown_goes_to_autre():
    r = triage.triage_ticket(t("Facture", "combien coûte mon forfait de cellulaire"), KB)
    assert r["categorie"] == "Autre" and r["escalade"] == "Oui"

def test_sample_file_runs():
    rows = list(csv.DictReader(open(Path(__file__).parent.parent / "sample_tickets.csv", encoding="utf-8")))
    assert len(rows) == 8 and all(triage.triage_ticket(x, KB)["categorie"] in triage.CATEGORIES for x in rows)
