## Installation 
pip install pandas




## Data
Place the 12 CSV files in a folder named `researchdata/` at the root of the project.




## How to run 
To run one of thee analyses from root, use the following command in your terminal :

```bash
python3 analyses/analysis_X.py
```

where X is the analyses you want to run (1, 2 or 3)




## How to interpret results
### Analyses 1  
You have the number of the participant and his/her average bpm


### Analyses 2
For each participant the analyse return : 
- the numbers of anomalys, 
- the date of each anomaly, 
- whether the bpm is too high or too low 

To determine if the BPM falls outside the normal range. I’ve compared it with an upper and a lower bound. These bounds were obtained with the participant average heart rate +/- a threshold selected to avoid overly broad or overly narrow detection. 

### Analyses 3
The regularity of each participant is calculated based on the similarity of effort between the days. The output shows if the participant is consistent or not showing : the number of the participant, and the number of cluster made with his data. The higher the number of cluster they have, the less they are consistent (no day is like an other) and vice versa. 




## Analysis 1 — Average Heart Rate Ranking


### Problem

My analysis calculates the average heart rate for each participant to identify issues such as a lack of physical activity (e.g., a heart rate that is too high is a heart that is not sufficiently conditioned), as well as to compare each participant’s heart rate with the others (to determine what is considered too high or too low).

### Algorithm

I used two algorithms. My sorting algorithm was a bubble sort, and my averaging algorithm was a linear scan.

### Why this algorithm ?

In this case, the bubble sort is appropriate because the number of participants isn't very large, so comparing them in pairs doesn't take much time. For linear scanning, this is the only way to calculate the average.

### Complexity

For space complexity, both algorithms operate in O(1) additional 
memory — the linear scan uses only two variables (sum, counter), 
and Bubble Sort sorts in-place without creating a new list.

For time complexity, the linear scan is O(N) where N = number 
of days (~290), and Bubble Sort is O(N²) where N = number 
of participants (12).




## Analysis 2 — Heart Rate Anomaly Detection


### Problem

This analysis identifies and lists heart rate anomalies over a given 
period. It can be used to detect potential health conditions 
(if anomalies increase over time) or to establish links 
between physical activity and heart rate irregularities.

### Algorithm

Two algorithms are combined:
- Linear scan to compute the average HR per participant.
- Two-pass scan to compare each day against the dynamic 
  baseline.

### Why these algorithms?

The linear scan is the natural choice for computing an average. 
The two-pass structure is appropriate because it avoids hardcoded 
medical thresholds. Each participant is compared to their own 
baseline, making the detection dynamic and personalised.

### Complexity

For space complexity, the linear scan operates in O(1) additional 
memory, it only uses two variables (sum, counter). The two-pass 
scan operates in O(N) space in the worst case, where all days are 
flagged as anomalies and stored as tuples.

For time complexity, both passes are O(N) where N = number of 
days per participant (~290), the first pass computes the average, 
the second compares each day to the dynamic baseline. The total 
complexity is therefore O(N).




## Analysis 3 — Day Similarity Graph BFS


### Problem

This analysis identifies patterns in the number of daily steps 
for each participant to determine whether their 
physical activity is consistent or not. By grouping days 
with similar step counts into clusters, we can assess 
a participant’s consistency: few clusters indicate 
consistent activity, while many clusters indicate 
inconsistent activity.

### Algorithm

Two algorithms are combined: "graph_builder" constructs a 
graph by connecting similar days with edges, and BFS 
traverses this graph to group connected days into clusters.

### Why these algorithms?

BFS is the natural method for forming clusters because it 
first explores all immediate neighbors before moving on.
DFS would unnecessarily go too deep, which is less suitable for 
clustering. graph_builder is effective because it structures the 
data into a graph, making navigation between similar days 
simple and logical.

### Complexity

For graph_builder: O(N²) time complexity because each day is compared 
to all the others; O(N²) space complexity in the worst case if all 
days are similar to one another.

For BFS: time complexity O(N + E), where E is the number of edges, 
space complexity O(N).

The total complexity is dominated by graph_builder: O(N²) 
in both time and space.
