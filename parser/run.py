import json

from page import Document

# EXTRACTING DATA
document = Document("data/document_1.pdf")


# CSV
print("Exporting to CSV...")

NULL_FILL = "NA"

subjects = {"Français Écrit", "Français Oral", "Philosophie", "Grand Oral"}

for page in document.pages:
    subjects.update([opt for opt in page.epreuves.options])
    if page.optionnel:
        subjects.update([f"Option: {opt}" for opt in page.optionnel.options])

subjects = list(subjects)
subjects.sort()

results = ['Nom et Prénom,"Classe","Code Postal",Genre,"Coefficient Épreuves","Points Épreuves","Coefficient Contrôle Continu","Points Contrôle Continu","Coefficient Options","Points Options","Points Jury","Coefficient Total","Points Total","' +
           '","'.join(subjects) + '"']
for page in document.pages:
    mention = page.mention if page.mention else NULL_FILL
    coeff_options = page.calcul_resultat.optionnel.coefficient if page.calcul_resultat.optionnel else NULL_FILL
    points_options = page.calcul_resultat.optionnel.points if page.calcul_resultat.optionnel and page.calcul_resultat.optionnel.coefficient > 0 else NULL_FILL
    points_jury = page.calcul_resultat.jury.points if page.calcul_resultat.jury and page.calcul_resultat.jury.coefficient > 0 else NULL_FILL
    result = f'"{page.last_name} {" ".join([n for n in page.first_names])}","{page.class_name}",{page.address.postal_code},{page.gender},{page.calcul_resultat.epreuves.coefficient},{page.calcul_resultat.epreuves.points},{page.calcul_resultat.controle_continu.coefficient},{page.calcul_resultat.controle_continu.points},{coeff_options},{points_options},{points_jury},{page.calcul_resultat.total.coefficient},{page.calcul_resultat.total.points}'
    for subject in subjects:
        result += ","
        if page.epreuves.options[0] == subject:
            result += str(page.epreuves.first_option.grade)
        elif page.epreuves.options[1] == subject:
            result += str(page.epreuves.second_option.grade)
        elif subject.startswith("Option:") and page.optionnel:
            subject = subject.removeprefix("Option: ")
            # print(page.optionnel.options)
            # print(page.optionnel.first_option, page.optionnel.second_option, page.optionnel.third_option)
            if len(page.optionnel.options) > 0 and page.optionnel.options[0] == subject and page.optionnel.first_option:
                result += str(page.optionnel.first_option.grade)
            elif len(page.optionnel.options) > 1 and page.optionnel.options[1] == subject and page.optionnel.second_option:
                result += str(page.optionnel.second_option.grade)
            elif len(page.optionnel.options) > 2 and page.optionnel.options[2] == subject and page.optionnel.third_option:
                result += str(page.optionnel.third_option.grade)
            else:
                result += NULL_FILL
        elif subject == "Français Écrit":
            result += str(page.epreuves.french_written.grade)
        elif subject == "Français Oral":
            result += str(page.epreuves.french_speaking.grade)
        elif subject == "Philosophie":
            result += str(page.epreuves.philosophy.grade)
        elif subject == "Grand Oral":
            result += str(page.epreuves.grand_oral.grade)
        else:
            result += NULL_FILL
    results.append(result)

with open("data/results.csv", "w") as f:
    f.write("\n".join(results))

# JSON
print("Exporting to JSON...")
with open("data/results.json", "w") as f:
    f.write(json.dumps([page.as_dict(camelCase=True) for page in document.pages], indent=4, ensure_ascii=False))
with open("website/data/results.json", "w") as f:
    f.write(json.dumps([page.as_dict(camelCase=True) for page in document.pages], indent=4, ensure_ascii=False))
