import csv
from collections import defaultdict

# Input and output paths
file_path = "arguments-training-with-topics.csv"
output_path = "topics_with_multiple_conclusions.txt"

# Dictionary to hold topics and their associated conclusions
topic_to_conclusions = defaultdict(set)

# Read the file
with open(file_path, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        topic = row['Topic'].strip()
        conclusion = row['Conclusion'].strip()
        topic_to_conclusions[topic].add(conclusion)

# Write results to a file
with open(output_path, "w", encoding='utf-8') as out:
    out.write("Topics with multiple distinct conclusions:\n\n")
    for topic, conclusions in topic_to_conclusions.items():
        if len(conclusions) > 1:
            out.write(f"Topic: {topic}\n")
            for c in conclusions:
                out.write(f"  - {c}\n")
            out.write("\n")

print(f"Results saved to '{output_path}'")
