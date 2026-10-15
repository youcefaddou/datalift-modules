"""Présentation de l'oral de validation Ydays 3 (16/12/2026), 10 minutes.

Usage : uv run --with python-pptx python docs/oral/build_oral_ydays3.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
OUT = HERE / "DataLift_oral_validation_16-12-2026.pptx"

# Couleurs du logo : bleu nuit dominant, indigo, bleu, cyan. Pas d'orange.
NAVY, INDIGO, BLUE, CYAN = "1A1D3A", "3A36C0", "2B6FD6", "1EB8D4"
INK2, TINT, WHITE, LINE = "5A5D72", "EEF3FB", "FFFFFF", "D5DCEB"
FONT = "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def rgb(h):
    return RGBColor.from_string(h)


def text(slide, x, y, w, h, runs, size=16, color=NAVY, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         italic=False, spacing=6):
    """runs : str, ou liste de paragraphes ; un paragraphe = str ou liste de (texte, {options})."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = [runs] if isinstance(runs, str) else runs
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(spacing)
        for t, o in ([(para, {})] if isinstance(para, str) else para):
            r = p.add_run()
            r.text = t
            f = r.font
            f.name, f.size = FONT, Pt(o.get("size", size))
            f.bold, f.italic = o.get("bold", bold), o.get("italic", italic)
            f.color.rgb = rgb(o.get("color", color))
    return tb


def box(slide, x, y, w, h, fill=TINT, radius=0.12, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.adjustments[0] = radius
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def badge(slide, x, y, label, size=0.62, fill=INDIGO, font=20):
    """Motif du deck : carré arrondi façon icône du logo."""
    box(slide, x, y, size, size, fill=fill, radius=0.28)
    text(slide, x, y, size, size, label, size=font, color=WHITE, bold=True, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE)


def arrow(slide, x, y, w=0.38, h=0.34, color=CYAN):
    s = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(color)
    s.line.fill.background()
    s.shadow.inherit = False


def content_slide(title):
    s = prs.slides.add_slide(BLANK)
    num = len(prs.slides._sldIdLst)
    text(s, 0.6, 0.45, 10.6, 0.8, title, size=34, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    s.shapes.add_picture(str(ASSETS / "logo_datalift.png"), Inches(11.35), Inches(0.55), height=Inches(0.42))
    text(s, 0.6, 7.0, 8, 0.3, "DataLift · Oral de validation · 16/12/2026", size=10, color=INK2)
    text(s, 11.9, 7.0, 0.8, 0.3, str(num), size=10, color=INK2, align=PP_ALIGN.RIGHT)
    return s


def dark_slide(lines):
    s = prs.slides.add_slide(BLANK)
    s.shapes.add_picture(str(ASSETS / "fond_sombre_datalift.png"), 0, 0, prs.slide_width, prs.slide_height)
    text(s, 0.6, 5.85, 12.1, 1.2, lines, size=20, color="C9D3EA", align=PP_ALIGN.CENTER)
    return s


# 1. Titre ------------------------------------------------------------------
dark_slide([[("Oral de validation · Ydays 3 · 16 décembre 2026", {"bold": True, "color": WHITE})],
            "Youcef Addou, Ilyes Chabab, Yannis Staali · pour l'équipe DataLift"])

# 2. Problème ---------------------------------------------------------------
s = content_slide("Des logiciels métier qui communiquent mal")
box(s, 0.6, 1.6, 4.3, 4.9, fill=NAVY)
text(s, 0.95, 2.1, 3.6, 1.6, "≈ 10", size=96, bold=True, color=CYAN)
text(s, 0.95, 3.85, 3.6, 2.4, ["logiciels métier dans une PME de 50 à 200 personnes",
                                [("factures, ERP, RH, recrutement, temps, frais, comptabilité", {"size": 14, "color": "C9D3EA"})]],
     size=20, color=WHITE, bold=True, spacing=12)
pains = [("Ressaisies", "Les mêmes données saisies plusieurs fois, dans plusieurs outils."),
         ("Exports Excel et scripts fragiles", "Des échanges bricolés qui cassent au moindre changement."),
         ("Migrations d'ERP risquées", "Reprise des données manuelle, erreurs découvertes après la bascule.")]
for i, (h, d) in enumerate(pains):
    y = 1.6 + i * 1.7
    box(s, 5.3, y, 7.4, 1.45)
    badge(s, 5.6, y + 0.41, str(i + 1))
    text(s, 6.5, y + 0.25, 6.0, 1.0, [[(h, {"bold": True, "size": 20})], [(d, {"size": 15, "color": INK2})]])

# 3. Migration et intégration ----------------------------------------------
s = content_slide("Migration et intégration : une même mécanique")
cols = [("Migration d'ERP", "Un flux exécuté une fois", "L'ancien logiciel vers le nouveau : reprise des données, contrôle, réconciliation.", INDIGO),
        ("Intégration", "Des flux récurrents", "Factures, collaborateurs, temps : échangés en continu entre les logiciels.", BLUE)]
for i, (h, sub, d, c) in enumerate(cols):
    x = 0.6 + i * 6.25
    box(s, x, 1.6, 5.85, 2.9, fill=TINT)
    badge(s, x + 0.35, 1.95, "↑" if i == 0 else "⇄", fill=c, font=24)
    text(s, x + 1.2, 1.95, 4.4, 0.62, [[(h, {"bold": True, "size": 24})]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.35, 2.85, 5.2, 1.5, [[(sub, {"bold": True, "size": 18, "color": c})], [(d, {"size": 16, "color": INK2})]])
box(s, 0.6, 4.85, 12.1, 1.75, fill=NAVY)
text(s, 0.95, 5.05, 11.4, 1.4,
     [[("Ce qui ne change pas depuis la fiche projet", {"bold": True, "color": CYAN, "size": 16})],
      [("Diagnostic qualité · mapping assisté par IA validé par un humain · réconciliation · tableau de bord", {"color": WHITE, "size": 20, "bold": True})]],
     spacing=8)

# 4. Fonctionnement ----------------------------------------------------------
s = content_slide("L'IA propose, l'humain valide")
steps = [("Connecter", "les logiciels via leurs API"), ("Réunir", "les données dans un modèle commun"),
         ("Demander", "en français, en une phrase"), ("Valider", "correspondances, score, explication"),
         ("Exécuter", "contrôler, réconcilier, alerter")]
for i, (h, d) in enumerate(steps):
    x = 0.6 + i * 2.5
    box(s, x, 1.75, 2.1, 2.75, fill=NAVY if i == 3 else TINT)
    badge(s, x + 0.25, 2.0, str(i + 1), fill=CYAN if i == 3 else INDIGO)
    dark = i == 3
    text(s, x + 0.25, 2.8, 1.7, 1.6, [[(h, {"bold": True, "size": 20, "color": WHITE if dark else NAVY})],
                                       [(d, {"size": 14, "color": "C9D3EA" if dark else INK2})]])
    if i < 4:
        arrow(s, x + 2.11, 2.95, w=0.36)
box(s, 0.6, 4.9, 12.1, 1.6, fill=TINT)
text(s, 0.95, 5.05, 11.4, 1.3,
     [[("Exemple de demande", {"bold": True, "size": 14, "color": INK2})],
      [("« Envoie les factures validées de Yooz vers IFS »", {"bold": True, "size": 24, "color": INDIGO, "italic": True})],
      [("Aucun flux n'est exécuté sans validation humaine enregistrée.", {"size": 14, "color": INK2})]], spacing=4)

# 5. Périmètre M1 ------------------------------------------------------------
s = content_slide("Périmètre M1 : 8 plateformes, 3 flux exécutés")
text(s, 0.6, 1.5, 5.6, 0.4, "Catalogue", size=18, bold=True, color=INK2)
plats = [("Yooz", "Factures"), ("IFS", "ERP"), ("Lucca", "SIRH"), ("Progessi", "Gestion d'affaires"),
         ("TeamTailor", "Recrutement"), ("Personio", "Temps"), ("Odoo", "Notes de frais"), ("Sage", "Comptabilité")]
for i, (n, d) in enumerate(plats):
    x, y = 0.6 + (i % 2) * 2.85, 2.0 + (i // 2) * 1.12
    key = n in ("Yooz", "IFS", "Lucca", "Progessi")
    box(s, x, y, 2.65, 0.95, fill=TINT if key else WHITE, line=None if key else LINE)
    text(s, x + 0.2, y + 0.12, 2.3, 0.75, [[(n, {"bold": True, "size": 17})], [(d, {"size": 13, "color": INK2})]], spacing=0)
text(s, 6.6, 1.5, 6, 0.4, "Flux exécutés de bout en bout", size=18, bold=True, color=INK2)
flux = [("1", "Yooz → IFS", "Factures fournisseurs rapprochées des commandes d'achat", "Indispensable", INDIGO),
        ("2", "Lucca → IFS", "Collaborateurs : créations, modifications, départs", "Indispensable", INDIGO),
        ("3", "Progessi → IFS", "Feuilles de temps validées, après le flux 2", "Important", BLUE)]
for i, (n, h, d, prio, c) in enumerate(flux):
    y = 2.0 + i * 1.5
    box(s, 6.6, y, 6.1, 1.3, fill=NAVY if i < 2 else TINT)
    badge(s, 6.85, y + 0.34, n, fill=c)
    dark = i < 2
    text(s, 7.7, y + 0.17, 4.9, 1.0,
         [[(h, {"bold": True, "size": 19, "color": WHITE if dark else NAVY}), (f"   {prio}", {"size": 13, "color": CYAN if dark else BLUE, "bold": True})],
          [(d, {"size": 14, "color": "C9D3EA" if dark else INK2})]], spacing=2)

# 5 bis. Vision sur 2 ans ----------------------------------------------------
s = content_slide("Vision sur 2 ans : prouver, puis étendre")
phases = [("2026-2027", "Prouver", ["Catalogue des 8 plateformes", "3 flux exécutés de bout en bout vers IFS",
                                          "Validation humaine, réconciliation, supervision", "Démo complète à l'oral final"], INDIGO),
          ("2027-2028", "Étendre", ["Nouveaux flux : TeamTailor → Lucca, Odoo → IFS, un flux vers Sage",
                                          "Modèle IA spécialisé pour les correspondances", "Socle analytique et tableau de bord avancé",
                                          "Assistant IA pour interroger les données"], BLUE)]
for i, (when, verb, items, c) in enumerate(phases):
    x = 0.6 + i * 6.25
    box(s, x, 1.55, 5.85, 4.0, fill=TINT)
    badge(s, x + 0.35, 1.85, "M" + str(i + 1), fill=c, font=18)
    text(s, x + 1.2, 1.85, 4.4, 0.62, [[(verb, {"bold": True, "size": 24}), (f"   {when}", {"size": 14, "color": INK2})]],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.35, 2.75, 5.2, 2.7, [[("•  ", {"color": c, "bold": True}), (it, {})] for it in items], size=16, spacing=8)
    if i == 0:
        arrow(s, 6.47, 3.35, w=0.36)
box(s, 0.6, 5.85, 12.1, 0.75, fill=NAVY)
text(s, 0.6, 5.85, 12.1, 0.75, "Un vrai produit data et IA, pensé pour pouvoir devenir une startup",
     size=19, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 6. Veille ------------------------------------------------------------------
s = content_slide("Veille de l'existant et notre angle")
text(s, 0.6, 1.5, 5.6, 0.4, "Ce qui existe", size=18, bold=True, color=INK2)
exist = [("Automatisation de flux", "n8n, Make : flux à construire soi-même"),
         ("Plateformes d'intégration", "Workato, Boomi : pensées pour les grands comptes"),
         ("Outils des éditeurs", "limités à leur propre écosystème"),
         ("Startups IA", "correspondance automatique de schémas")]
for i, (h, d) in enumerate(exist):
    y = 2.0 + i * 1.12
    box(s, 0.6, y, 5.6, 0.95, fill=WHITE, line=LINE)
    text(s, 0.85, y + 0.12, 5.2, 0.75, [[(h, {"bold": True, "size": 16})], [(d, {"size": 13, "color": INK2})]], spacing=0)
box(s, 6.6, 1.5, 6.1, 5.0, fill=NAVY)
text(s, 6.95, 1.8, 5.5, 0.5, "Notre angle", size=20, bold=True, color=CYAN)
angle = ["PME de 50 à 200 personnes", "Logiciels utilisés en France", "L'IA propose, l'humain valide",
         "Supervision et réconciliation intégrées", "Briques open source réutilisées"]
for i, a in enumerate(angle):
    y = 2.5 + i * 0.78
    badge(s, 6.95, y, "✓", size=0.5, fill=BLUE, font=16)
    text(s, 7.65, y, 4.9, 0.5, a, size=18, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# 7. Architecture ------------------------------------------------------------
s = content_slide("Architecture : données et contrôle")
text(s, 0.6, 1.5, 8, 0.4, "Plan de données", size=18, bold=True, color=INK2)
pipe = [("API source", "Yooz, Lucca, Progessi", WHITE), ("Bronze", "brut, horodaté", TINT),
        ("Silver", "modèle commun, contrôlé", TINT), ("Gold", "vues, réconciliation", TINT), ("API cible", "IFS", WHITE)]
for i, (h, d, f) in enumerate(pipe):
    x = 0.6 + i * 2.5
    box(s, x, 2.0, 2.1, 1.45, fill=NAVY if h == "Silver" else f, line=LINE if f == WHITE else None)
    dark = h == "Silver"
    text(s, x + 0.2, 2.2, 1.75, 1.1, [[(h, {"bold": True, "size": 19, "color": WHITE if dark else NAVY})],
                                       [(d, {"size": 13, "color": "C9D3EA" if dark else INK2})]], spacing=2)
    if i < 4:
        arrow(s, x + 2.11, 2.55, w=0.36)
text(s, 0.6, 3.6, 12.1, 0.4, "Lignage sur chaque donnée silver : source_system, source_id, extracted_at", size=14, color=INDIGO, bold=True)
text(s, 0.6, 4.15, 8, 0.4, "Plan de contrôle", size=18, bold=True, color=INK2)
ctrl = ["Catalogue", "Agent IA", "Validation", "Orchestrateur", "Supervision"]
for i, c in enumerate(ctrl):
    x = 0.6 + i * 2.5
    box(s, x, 4.6, 2.1, 0.8, fill=INDIGO)
    text(s, x, 4.6, 2.1, 0.8, c, size=17, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 5.75, 12.1, 0.9,
     [[("Stack : ", {"bold": True}), ("Python 3.12, Pydantic, FastAPI, PostgreSQL, Microsoft Fabric (repli DuckDB), Docker, Terraform, GitHub Actions", {"color": INK2})]],
     size=15)

# 8. Données synthétiques ---------------------------------------------------
s = content_slide("Des données synthétiques, jamais réelles")
text(s, 0.6, 1.5, 5.8, 0.4, "Les objets des 3 flux", size=18, bold=True, color=INK2)
objs = ["Fournisseurs", "Commandes d'achat", "Factures et lignes", "Collaborateurs", "Projets", "Feuilles de temps"]
for i, o in enumerate(objs):
    x, y = 0.6 + (i % 2) * 2.95, 2.0 + (i // 2) * 1.2
    box(s, x, y, 2.75, 1.0, fill=TINT)
    text(s, x + 0.25, y, 2.3, 1.0, o, size=17, bold=True, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 5.75, 5.65, 0.8, "Générées depuis les spécifications d'API, servies par des API simulées.", size=15, color=INK2)
box(s, 6.6, 1.5, 6.1, 5.0, fill=NAVY)
text(s, 6.95, 1.8, 5.5, 0.5, "Défauts injectés et documentés", size=20, bold=True, color=CYAN)
defects = ["Doublons", "Montants incohérents", "Facture sans commande", "Fournisseur inconnu",
           "Collaborateur absent d'IFS", "Heures hors limites", "Champs manquants"]
text(s, 6.95, 2.45, 5.5, 3.9, [[("•  ", {"color": CYAN, "bold": True}), (d, {})] for d in defects],
     size=18, color=WHITE, spacing=8)

# 9. Agent IA ----------------------------------------------------------------
s = content_slide("L'agent IA : comprendre, proposer, expliquer")
flow = [("Demande", "en français"), ("Compréhension", "source, cible, objet, filtre"),
        ("Correspondances", "champ à champ, score de confiance"), ("Explication", "pour chaque champ")]
for i, (h, d) in enumerate(flow):
    x = 0.6 + i * 3.1
    box(s, x, 1.65, 2.7, 2.0, fill=TINT)
    badge(s, x + 0.25, 1.9, str(i + 1), fill=BLUE)
    text(s, x + 0.25, 2.65, 2.3, 0.95, [[(h, {"bold": True, "size": 18})], [(d, {"size": 13, "color": INK2})]], spacing=0)
    if i < 3:
        arrow(s, x + 2.72, 2.35, w=0.36)
kpis = [("≥ 80 %", "de correspondances correctes sur le jeu de test"), ("8 × 8", "toute paire du catalogue couverte"),
        ("100 %", "des propositions validées par un humain")]
for i, (k, d) in enumerate(kpis):
    x = 0.6 + i * 4.1
    box(s, x, 4.0, 3.8, 2.5, fill=NAVY)
    text(s, x + 0.3, 4.25, 3.3, 2.2, [[(k, {"bold": True, "size": 44, "color": CYAN})], [(d, {"size": 16, "color": WHITE})]], spacing=4)

# 10. Équipe -----------------------------------------------------------------
s = content_slide("L'équipe")
team = [("YA", "Youcef Addou", "Chef de projet et architecte data", INDIGO), ("IC", "Ilyes Chabab", "Data engineering", BLUE),
        ("YS", "Yannis Staali", "Intelligence artificielle", BLUE), ("YM", "Yasser Moulfi", "Infra et cloud", CYAN),
        ("AK", "Asmae Kaysouny", "IA et data", BLUE), ("NA", "Ndeye Aida Ndour", "IA et data", BLUE)]
for i, (ini, n, r, c) in enumerate(team):
    x, y = 0.6 + (i % 3) * 4.1, 1.65 + (i // 3) * 2.5
    box(s, x, y, 3.8, 2.2, fill=TINT)
    badge(s, x + 0.35, y + 0.4, ini, size=1.0, fill=c, font=26)
    text(s, x + 1.6, y + 0.4, 2.1, 1.5, [[(n, {"bold": True, "size": 19})], [(r, {"size": 15, "color": INK2})]], spacing=2)

# 11. Organisation -----------------------------------------------------------
s = content_slide("Organisation : Scrum, Jira et 8 sprints")
s.shapes.add_picture(str(ASSETS / "gantt_datalift_m1.png"), Inches(0.45), Inches(1.35), width=Inches(9.9))
stats = [("8", "sprints"), ("13", "épopées"), ("94", "tickets Jira"), ("37 / 37", "exigences couvertes")]
for i, (k, d) in enumerate(stats):
    y = 1.45 + i * 1.28
    box(s, 10.55, y, 2.15, 1.12, fill=NAVY if i == 3 else TINT)
    dark = i == 3
    text(s, 10.75, y + 0.12, 1.85, 0.9, [[(k, {"bold": True, "size": 28, "color": CYAN if dark else INDIGO})],
                                         [(d, {"size": 13, "color": WHITE if dark else INK2})]], spacing=0)

# 12. Risques et prochaines étapes --------------------------------------------
s = content_slide("Risques maîtrisés et prochaines étapes")
risks = [("Capacité", "L'équipe travaille une journée par sprint : tickets courts, finis dans la journée."),
         ("Flux 3", "En cas de retard, il est montré au niveau du catalogue. Les flux 1 et 2 ne sont pas négociables."),
         ("Décisions ouvertes", "Orchestration, interface, modèle IA, accès Fabric : tranchées par écrit avant le sprint concerné.")]
for i, (h, d) in enumerate(risks):
    y = 1.6 + i * 1.65
    box(s, 0.6, y, 6.6, 1.45)
    badge(s, 0.9, y + 0.41, "!", fill=INDIGO)
    text(s, 1.8, y + 0.2, 5.2, 1.1, [[(h, {"bold": True, "size": 19})], [(d, {"size": 14, "color": INK2})]], spacing=2)
box(s, 7.6, 1.6, 5.1, 4.75, fill=NAVY)
text(s, 7.95, 1.85, 4.5, 0.5, "Prochains jalons", size=20, bold=True, color=CYAN)
miles = [("20/01", "Données chargées et profilées"), ("21/01", "Rapport de qualité v1"), ("03/03", "Mapping IA v1 mesuré")]
for i, (d, l) in enumerate(miles):
    y = 2.6 + i * 1.15
    badge(s, 7.95, y, "↑", size=0.6, fill=BLUE, font=20)
    text(s, 8.75, y - 0.05, 3.8, 0.75, [[(d, {"bold": True, "size": 20, "color": WHITE})], [(l, {"size": 14, "color": "C9D3EA"})]], spacing=0)

# 13. Fin --------------------------------------------------------------------
dark_slide([[("Merci. Vos questions ?", {"bold": True, "color": WHITE, "size": 26})]])

# Notes de présentation : puces courtes, une liste par slide ------------------
NOTES = [
    ["Youcef · 20 s", "Bonjour, équipe DataLift", "Plan : problème, solution, périmètre, vision, architecture, IA, équipe, planning"],
    ["Youcef · 1 min", "PME de 50 à 200 personnes : une dizaine de logiciels", "Ressaisies, exports Excel, scripts fragiles",
     "Moment le plus risqué : changer d'ERP, reprise des données à la main"],
    ["Youcef · 1 min", "La fiche projet parlait de migration d'ERP : c'est toujours le cas",
     "Une migration = un flux exécuté une seule fois", "Le même moteur gère aussi les échanges récurrents",
     "Livrables annoncés conservés : qualité, mapping IA, réconciliation, tableau de bord"],
    ["Youcef · 1 min", "5 étapes : connecter, réunir, demander, valider, exécuter", "L'utilisateur écrit en français",
     "L'IA propose avec un score et une explication", "Rien ne s'exécute sans validation humaine (cohérent avec l'AI Act)"],
    ["Youcef · 45 s", "8 plateformes au catalogue : l'IA propose des correspondances entre toutes",
     "3 flux exécutés de bout en bout, tous vers IFS", "Flux 1 et 2 indispensables, flux 3 après le flux 2"],
    ["Youcef · 45 s", "M1 : prouver sur 3 flux réels de bout en bout",
     "M2 : plus de flux, IA spécialisée, analytique, assistant IA", "Ambition : un produit qui peut devenir une startup"],
    ["Youcef · 45 s", "L'existant est riche, on ne le nie pas",
     "Notre angle : PME, logiciels français, humain qui valide, supervision intégrée",
     "On réutilise l'open source au lieu de tout recréer"],
    ["Ilyes · 1 min", "Plan de données : bronze, silver, gold", "Bronze : copie brute, jamais modifiée",
     "Silver : modèle commun contrôlé, origine tracée sur chaque donnée", "Gold : vues et réconciliation",
     "Plan de contrôle : catalogue, IA, validation, orchestration, supervision"],
    ["Ilyes · 45 s", "Aucune donnée réelle", "Les objets des 3 flux, générés depuis les specs",
     "Défauts injectés volontairement et documentés", "But : mesurer ce que DataLift détecte"],
    ["Yannis · 1 min 15", "Comprend la demande : source, cible, objet, filtre", "Propose champ à champ avec un score de confiance",
     "Explique chaque proposition", "Objectif : au moins 80 % de bonnes correspondances, mesuré sur un jeu de référence",
     "Choix du modèle (API ou local) tranché avant le sprint 3"],
    ["Youcef · 30 s", "6 personnes : 1 chef de projet, 1 infra et cloud, 4 IA et data", "Rôles détaillés attribués le 25/11"],
    ["Youcef · 1 min", "Scrum : 8 sprints calés sur les journées Ydays",
     "Jira : 13 épopées, 94 tickets, chacun relié au cahier des charges", "Une tâche = une branche = une PR",
     "Deux jalons : aujourd'hui et l'oral final du 27/05"],
    ["Youcef · 45 s", "Capacité : une journée par sprint, donc des tickets courts", "Flux 3 en retard : montré au niveau du catalogue",
     "Décisions ouvertes tranchées par écrit (ADR)", "Prochains jalons : 20/01, 21/01, 03/03"],
    ["Youcef", "Ouvrir les questions", "Ilyes : données et architecture", "Yannis : IA"],
]
assert len(NOTES) == len(prs.slides._sldIdLst), (len(NOTES), len(prs.slides._sldIdLst))
for slide, lines in zip(prs.slides, NOTES):
    slide.notes_slide.notes_text_frame.text = "\n".join("• " + line for line in lines)

prs.save(OUT)
print(OUT)
