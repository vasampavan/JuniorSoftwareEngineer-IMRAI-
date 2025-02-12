import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
file = "server.log"
pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(INFO|WARNING|ERROR)\] (.+)"
logs = []
with open(file, "r") as file:
    for i in file:
        match = re.match(pattern, i)
        if match:
            logs.append(list(match.groups()))

df = pd.DataFrame(logs, columns=["Timestamp", "Level", "Message"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
data = df[df["Level"] == "ERROR"]["Message"].value_counts()
print("\nTop 5 frequent errors are:")
print(data.head(5))
plt.figure(figsize=(10, 5))
data.head(5).plot(kind="bar", color="red")
plt.title("Most frequent errors")
plt.xlabel("Error message")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.grid()
plt.show()
df["Hour"] = df["Timestamp"].dt.floor("H")
trends = df.groupby(["Hour", "Level"]).size().unstack().fillna(0)
plt.figure(figsize=(12, 6))
trends.plot(ax=plt.gca(), marker="o")
plt.title("Log level trends over time")
plt.xlabel("Time")
plt.ylabel("Log count")
plt.grid()
plt.legend(title="Log level")
plt.xticks(rotation=45)
plt.show()
threshold = trends["ERROR"].mean() + 2 * trends["ERROR"].std()
anomalies = trends[trends["Error"] > threshold]
print("\nAnomalous hours with high errors:")
print(anomalies)
warnings = df[df["Level"] == "WARNING"]["Message"].value_counts()
print("\nTop 5 Frequent Warnings:")
print(warnings.head(5))
patterns = ["memory", "disk", "network", "database", "security"]
for i in patterns:
    count = df[df["Message"].str.contains(i, case=False, na=False)].shape[0]
    print(f"{i.capitalize()}-related issues: {count}")