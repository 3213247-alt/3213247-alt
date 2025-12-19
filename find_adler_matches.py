import csv

def get_best_matches():
    target_count = 16412
    matches = []
    with open('Names_2010Census.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['name'] == 'ADLER': continue
            try:
                cnt = int(row['count'])
                diff = abs(cnt - target_count)
                if diff < 200:
                    matches.append({
                        'name': row['name'].title(),
                        'count': cnt,
                        'rank': int(row['rank']),
                        'prop': float(row['prop100k']),
                        'diff': diff
                    })
            except: pass
    
    matches.sort(key=lambda x: x['diff'])
    return matches[:50]

best = get_best_matches()
print("Rank|Name|Count|US Rank|Prop100k")
print("---|---|---|---|---")
for i, m in enumerate(best):
    print(f"{i+1}|{m['name']}|{m['count']}|{m['rank']}|{m['prop']}")
