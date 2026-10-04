import pandas as pd
import os

resultats = []


def moyenne_hr(df):
    somme = 0
    nb_jours = 0
    for value in df["ACTIVITY_hr_average"]:
        if pd.notna(value):
            somme += value
            nb_jours += 1
    moyenne = somme / nb_jours
    return int(moyenne)


def classement(liste):
    n = len(liste)
    for i in range(n):
        for j in range(n - i - 1):
            if liste[j][1] < liste[j + 1][1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
    return liste


directory = os.path.join(os.path.dirname(__file__), "..", "researchdata")
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        full_path = os.path.join(directory, filename)
        donnees = pd.read_csv(full_path)
        participant_id = filename.replace(".csv", "")
        moyenne = moyenne_hr(donnees)
        resultats.append((participant_id, moyenne))


for participant_id, moyenne in resultats:
    print(f"Participant {participant_id} a une moyenne de {moyenne} bpm.")


# Built-in comparison
resultats_copy = resultats.copy()
resultats_builtin = sorted(resultats_copy, key=lambda x: x[1], reverse=True)
resultats_manuel = classement(resultats.copy())

assert [x[1] for x in resultats_manuel] == [x[1] for x in resultats_builtin], \
    "Le classement manuel diffère du built-in !"
print("Built-in comparison succeeded !")


# Tests

# Passing test
df_test = pd.DataFrame({"ACTIVITY_hr_average": [60, 70, 80, float("nan"), 90]})
assert moyenne_hr(df_test) == 75, "La moyenne devrait être 75"
print("Passing test succeeded !")

# Failing test
liste_test = [("A", 10), ("B", 30), ("C", 20)]
assert classement(liste_test) == [("A", 10), ("B", 30), ("C", 20)], "Ordre croissant attendu (test qui échoue)"
print("This line will NOT be reached.")