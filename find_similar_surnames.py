import csv

target_count = 16412
target_rank = 2223
us_pop_2010 = 308745538

def calculate_user_prop(count):
    return (float(count) / us_pop_2010) * 100

data = []
adler_found = False

with open('data/Names_2010Census.csv', 'r') as f:
    # Handle the fact that the first few lines might be empty or header might be tricky
    # The head command showed: name,rank,count,prop100k,...
    reader = csv.DictReader(f)
    for row in reader:
        try:
            name = row['name']
            rank = int(row['rank'])
            count = int(row['count'])
            # prop100k = float(row['prop100k'])
            
            # Store necessary data
            data.append({
                'name': name,
                'rank': rank,
                'count': count,
                'diff': abs(count - target_count)
            })
            
            if name == 'ADLER':
                adler_found = True
        except ValueError:
            continue

# Sort by difference in count
sorted_data = sorted(data, key=lambda x: x['diff'])

# Select top 50 (excluding ADLER itself if we want, but let's keep it to show the match)
# The user wants "Adler alike", so we exclude Adler.
matches = [d for d in sorted_data if d['name'] != 'ADLER'][:50]

print(f"{'Name':<20} | {'Rank':<10} | {'Count':<10} | {'US Prop (%)':<15}")
print("-" * 65)

for m in matches:
    us_prop = calculate_user_prop(m['count'])
    print(f"{m['name']:<20} | {m['rank']:<10} | {m['count']:<10} | {us_prop:.4f}%")
