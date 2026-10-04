import pandas as pd
import os

resultats = []


def graph_builder(df, seuil):
    graphe = {}
    for i in range(len(df)):
        steps_i = df["ACTIVITY_steps"][i]
        graphe[i] = []
        for j in range(len(df)):
            steps_j = df["ACTIVITY_steps"][j]
            if i != j and abs(steps_i - steps_j) <= seuil:
                graphe[i].append(j)
    return graphe


def BFS(graphe, start):
    queue = [start]
    visités = {}
    cluster = []
    while len(queue) > 0:
        actuel = queue.pop(0)
        for voisin in graphe[actuel]:
            if voisin not in visités:
                visités[voisin] = True
                cluster.append(voisin)
                queue.append(voisin)
    return cluster


def analyser(df, seuil):
    graphe = graph_builder(df, seuil)
    clusters = []
    visités = {}
    for i in range(len(df)):
        if i not in visités:
            cluster = BFS(graphe, i)
            clusters.append(cluster)
            for noeud in cluster:
                visités[noeud] = True

    somme = 0
    for cluster in clusters:
        somme += len(cluster)
    moyenne_taille = somme / len(clusters) if clusters else 0

    if len(clusters) <= 6:
        return ("régulier", len(clusters), moyenne_taille)
    else:
        return ("irrégulier", len(clusters), moyenne_taille)


directory = os.path.join(os.path.dirname(__file__), "..", "researchdata")
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        full_path = os.path.join(directory, filename)
        donnees = pd.read_csv(full_path)
        participant_id = filename.replace(".csv", "")
        resultat = analyser(donnees, seuil=500)
        resultats.append((participant_id, resultat))


for participant_id, resultat in resultats:
    verdict, nb_clusters, moyenne = resultat
    print(
        f"Participant {participant_id} — {verdict} ({nb_clusters} clusters, moyenne {moyenne:.1f} jours/cluster)"
    )


# Tests

# Passing test 
df_test = pd.DataFrame({"ACTIVITY_steps": [1000, 1200, 5000]})
# |1000-1200| = 200 <= 500 → noeud 0 et 1 sont voisins
# |1000-5000| = 4000 > 500 → noeud 0 et 2 ne sont pas voisins
graphe_test = graph_builder(df_test, seuil=500)
assert 1 in graphe_test[0], "Le noeud 1 devrait être voisin du noeud 0"
print("Passing test succeeded !")

# Failing test 
assert 2 in graphe_test[0], "Le noeud 2 devrait être voisin du noeud 0 (test qui échoue)"
print("This line will NOT be reached.")