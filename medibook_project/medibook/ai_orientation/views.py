from django.shortcuts import render

from doctors.models import Specialite
from .models import AnalyseSymptome
from patients.models import ProfilPatient

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    TfidfVectorizer = None
    cosine_similarity = None

SYMPTOM_KEYWORDS = {
    "cardiologie": ["coeur", "poitrine", "palpitation", "tension"],
    "dermatologie": ["peau", "bouton", "eczema", "allergie"],
    "pediatrie": ["enfant", "bebe", "nourrisson", "croissance"],
    "neurologie": ["migraine", "tete", "vertige", "convulsion"],
    "ophtalmologie": ["oeil", "vision", "vue", "larmoiement"],
}


def analyse_par_keywords(texte, specialites):
    best_name = None
    best_score = 0
    texte_normalise = texte.lower()
    for specialite_name, keywords in SYMPTOM_KEYWORDS.items():
        score = sum(keyword in texte_normalise for keyword in keywords)
        if score > best_score and specialite_name in specialites:
            best_name = specialite_name
            best_score = score
    return specialites.get(best_name), round((best_score / 4) * 100, 2) if best_score else (None, 25.0)


def analyser_symptomes(request):
    resultat = None

    if request.method == "POST":
        texte = request.POST.get("texte_symptomes", "").strip()
        specialites = list(Specialite.objects.all())
        specialite = None
        confiance = 25.0

        if texte and specialites and TfidfVectorizer is not None:
            corpus = [spec.description or spec.name for spec in specialites] + [texte]
            vectorizer = TfidfVectorizer(stop_words="french")
            matrix = vectorizer.fit_transform(corpus)
            scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
            best_index = int(scores.argmax())
            specialite = specialites[best_index]
            confiance = round(float(scores[best_index]) * 100, 2)
        elif texte:
            specialites_map = {spec.name.lower(): spec for spec in specialites}
            specialite, confiance = analyse_par_keywords(texte, specialites_map)
            specialite = specialite or (specialites[0] if specialites else None)

        patient = ProfilPatient.objects.order_by("id").first()

        if texte and specialite:
            resultat = AnalyseSymptome.objects.create(
                patient=patient,
                texte_symptomes=texte,
                specialite_recommandee=specialite,
                score_confiance=confiance,
            )

    return render(request, "ai_orientation/analyser.html", {"resultat": resultat})


def historique_ia(request):
    analyses = AnalyseSymptome.objects.all().order_by("-cree_le")
    return render(request, "historique.html", {"analyses": analyses})
