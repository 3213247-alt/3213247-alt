import csv

target_name = "ADLER"
data = []

with open('Names_2010Census.csv', 'r') as f:
    reader = csv.DictReader(f)
    # Strip whitespace from headers just in case
    reader.fieldnames = [h.strip() for h in reader.fieldnames]
    
    for row in reader:
        # Some rows might be summary or empty, check if 'count' exists
        if row['name'] and row['count']:
            try:
                row['count'] = int(row['count'].replace(',', ''))
                row['rank'] = int(row['rank'].replace(',', ''))
                # prop100k might be float
                data.append(row)
            except ValueError:
                continue

# Find Adler
adler = next((item for item in data if item['name'] == target_name), None)

if adler:
    print(f"Adler found: Rank={adler['rank']}, Count={adler['count']}")
    
    # Calculate diff
    for item in data:
        item['diff'] = abs(item['count'] - adler['count'])
        
    # Sort by diff
    # We exclude Adler itself from the list of "matches" usually, but user said "Adler name if not exactly than very close"
    # I'll keep Adler in the list to show position, or remove if strictly requesting *other* names.
    # User: "List 12 that are very very close. choose one that true"
    
    sorted_data = sorted(data, key=lambda x: x['diff'])
    
    print("\nTop 15 Closest Matches by Count:")
    print(f"{'NAME':<15} {'RANK':<10} {'COUNT':<10} {'PROP100k':<10} {'DIFF':<10}")
    for item in sorted_data[:15]:
        print(f"{item['name']:<15} {item['rank']:<10} {item['count']:<10} {item['prop100k']:<10} {item['diff']:<10}")

else:
    print("Adler not found in data.")
