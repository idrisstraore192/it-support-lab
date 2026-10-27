#!/usr/bin/env python3
"""Triage de tickets de soutien TI assisté par IA.

Deux modes :
  - règles (par défaut) : fonctionne hors ligne, sans clé API ;
  - IA (si ANTHROPIC_API_KEY est défini et le paquet `anthropic` installé) :
    un modèle de langage classe le ticket et rédige une réponse, qui est
    ensuite validée contre les catégories connues.
Dans les deux cas la base de connaissances (kb.json) fournit les étapes
de résolution. Les données d'exemple sont fictives : ne jamais envoyer de
données réelles ou confidentielles à un service externe.
"""
import argparse, csv, json, os, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).parent
URGENT_WORDS = ["urgent", "production", "tout le service", "tous les", "panne générale", "rançon", "piratage", "arrêtée", "arret"]
HIGH_WORDS = ["impossible", "bloqué", "hameçonnage", "phishing", "j'ai cliqué", "peut-être cliqué", "plus d'accès", "toute l'équipe"]
CATEGORIES = ["Compte et accès", "Réseau", "Impression", "Courriel et Microsoft 365", "Poste de travail", "Logiciel et applications", "Sécurité", "Autre"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def load_kb(path=HERE / "kb.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def score_article(text: str, article: dict) -> int:
    t = norm(text)
    return sum(1 for k in article["keywords"] if norm(k) in t)


def classify_rules(text: str, kb):
    scores = [(score_article(text, a), a) for a in kb]
    best_score, best = max(scores, key=lambda x: x[0])
    if best_score == 0:
        return "Autre", None
    # La sécurité prime si un indice d'hameçonnage est présent.
    sec = [a for s, a in scores if a["category"] == "Sécurité" and s > 0]
    if sec:
        return "Sécurité", sec[0]
    return best["category"], best


def priority_rules(text: str, category: str) -> str:
    t = norm(text)
    if any(norm(w) in t for w in URGENT_WORDS):
        return "P1 - Urgent"
    if category == "Sécurité" or any(norm(w) in t for w in HIGH_WORDS):
        return "P2 - Élevée"
    if category == "Autre":
        return "P4 - Faible"
    return "P3 - Normale"


def llm_triage(text: str):
    """Retourne (catégorie, priorité, réponse) via l'API Claude, ou None si indisponible."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    try:
        import anthropic
    except ImportError:
        return None
    client = anthropic.Anthropic(api_key=key)
    prompt = (
        "Tu es un agent de soutien TI de niveau 1. Réponds UNIQUEMENT en JSON avec les clés "
        '"categorie", "priorite" et "reponse". '
        f"categorie doit être l'une de : {CATEGORIES}. priorite : P1 - Urgent, P2 - Élevée, P3 - Normale ou P4 - Faible. "
        "reponse : un court message poli en français à l'utilisateur (max 60 mots), sans demander de mot de passe.\n\nTicket :\n" + text
    )
    msg = client.messages.create(model=os.environ.get("TRIAGE_MODEL", "claude-sonnet-4-5"), max_tokens=400,
                                 messages=[{"role": "user", "content": prompt}])
    raw = msg.content[0].text
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    data = json.loads(m.group(0))
    cat = data.get("categorie")
    pri = data.get("priorite")
    if cat not in CATEGORIES or pri not in ("P1 - Urgent", "P2 - Élevée", "P3 - Normale", "P4 - Faible"):
        return None  # sortie invalide : on retombe sur les règles
    return cat, pri, str(data.get("reponse", ""))[:600]


def triage_ticket(ticket: dict, kb, use_ai=False):
    text = f"{ticket['sujet']}. {ticket['description']}"
    category, article = classify_rules(text, kb)
    priority = priority_rules(text, category)
    reply, mode = "", "règles"
    if use_ai:
        res = llm_triage(text)
        if res:
            category, priority, reply = res
            mode = "IA"
            article = next((a for a in kb if a["category"] == category), article)
    if not reply:
        reply = "Bonjour, nous avons bien reçu votre demande et nous l'analysons. Nous vous revenons rapidement."
    return {
        "id": ticket["id"], "sujet": ticket["sujet"], "categorie": category, "priorite": priority,
        "mode": mode, "article_kb": article["id"] if article else "",
        "etapes_suggerees": " | ".join(article["steps"]) if article else "Escalader : aucun article correspondant.",
        "reponse_proposee": reply,
        "escalade": "Oui" if priority.startswith(("P1", "P2")) or not article else "Non",
    }


def main():
    ap = argparse.ArgumentParser(description="Triage de tickets TI assisté par IA")
    ap.add_argument("csv", nargs="?", default=str(HERE / "sample_tickets.csv"))
    ap.add_argument("--ai", action="store_true", help="utiliser un modèle IA si une clé API est configurée")
    ap.add_argument("--out", default="triage_report.csv")
    a = ap.parse_args()
    kb = load_kb()
    with open(a.csv, newline="", encoding="utf-8") as f:
        tickets = list(csv.DictReader(f))
    rows = [triage_ticket(t, kb, a.ai) for t in tickets]
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(f"{r['id']} | {r['priorite']:<12} | {r['categorie']:<26} | escalade: {r['escalade']} | {r['mode']}")
    print(f"\nRapport écrit dans {a.out}")


if __name__ == "__main__":
    sys.exit(main())
