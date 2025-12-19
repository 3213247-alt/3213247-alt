import csv

target_count = 16412
target_rank = 2223
# Adler stats
# ADLER,2223,16412,5.56,50610.34,94.9,0.57,0.71,0.15,1.06,2.61

candidates = []

with open('Names_2010Census.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            count = int(row['count'])
            rank = int(row['rank'])
            pctwhite = float(row['pctwhite']) if row['pctwhite'] != '(S)' else 0
            pctblack = float(row['pctblack']) if row['pctblack'] != '(S)' else 0
            pcthispanic = float(row['pcthispanic']) if row['pcthispanic'] != '(S)' else 0
            
            # Filter for Adler-like demographics (European/White)
            # Relaxed filter slightly to ensure we get enough candidates
            if pctwhite > 85 and pctblack < 5 and pcthispanic < 5:
                candidates.append({
                    'name': row['name'],
                    'rank': rank,
                    'count': count,
                    'pctwhite': pctwhite,
                    'diff': abs(count - target_count)
                })
        except ValueError:
            continue

# Sort by count difference
candidates.sort(key=lambda x: x['diff'])

# Print top 150
print(f"{'NAME':<15} {'RANK':<10} {'COUNT':<10} {'DIFF':<10} {'PCT_WHITE':<10}")
print("-" * 60)
for c in candidates[:150]:
    print(f"{c['name']:<15} {c['rank']:<10} {c['count']:<10} {c['diff']:<10} {c['pctwhite']:<10}")
