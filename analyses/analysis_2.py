import pandas as pd
import os

an = []


def moyenne_hr(df):
    somme = 0
    nb_jours = 0
    for value in df["ACTIVITY_hr_average"]:
        if pd.notna(value):
            somme += value
            nb_jours += 1
    moyenne = somme / nb_jours
    return int(moyenne)


def detection_an(df, moyenne, seuil=15):
    borne_haute = moyenne + seuil
    borne_basse = moyenne - seuil
    anomalies = []

    for i in range(len(df)):
        value = df["ACTIVITY_hr_average"][i]
        date = df["DATE"][i]

        if pd.notna(value):
            if value >= borne_haute:
                anomalies.append((int(value), date, "trop élevé"))
            elif value <= borne_basse:
                anomalies.append((int(value), date, "trop faible"))

    return anomalies


directory = os.path.join(os.path.dirname(__file__), "..", "researchdata")
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        full_path = os.path.join(directory, filename)
        donnees = pd.read_csv(full_path)
        participant_id = filename.replace(".csv", "")
        moyenne = moyenne_hr(donnees)
        anomalies = detection_an(donnees, moyenne, seuil=15)
        an.append((participant_id, anomalies))

for participant_id, anomalies in an:
    print(f"\n\n\nParticipant {participant_id} — {len(anomalies)} anomalie(s) :\n")
    for value, date, statut in anomalies:
        print(f"-{date} : {value} bpm ({statut})")


# Tests

# --- Passing test ---
df_test = pd.DataFrame({
    "ACTIVITY_hr_average": [70, 70, 70, 90, 50],
    "DATE": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
})
anomalies_test = detection_an(df_test, 70, seuil=15)
assert len(anomalies_test) == 2, f"Attendu 2 anomalies, obtenu {len(anomalies_test)}"
print("Passing test succeeded !")

# --- Failing test ---
assert len(anomalies_test) == 0, "Attendu 0 anomalie (test qui échoue)"
print("This line will NOT be reached.")