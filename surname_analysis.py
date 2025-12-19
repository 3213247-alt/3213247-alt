#!/usr/bin/env python3
"""
Surname Analysis: Finding Statistical Matches to ADLER
=====================================================
Target Metrics (from 2010 U.S. Census):
- Count: 16,412
- Rank: 2,223
- Proportion: 5.56 per 100,000 (0.00556%)
- Demographics: 94.9% White

UK Estimate (unverified): ~0.004% (~4 per 100,000)

We need surnames matching across 4 metrics:
1. U.S. Count (~16,412)
2. U.S. Rank (~2,223)
3. U.S. Proportion (~5.56 per 100k)
4. Similar origin/distribution pattern (proxy for UK similarity)
"""

import csv

# Read the census data
surnames = []
with open('/workspace/Names_2010Census.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            surnames.append({
                'name': row['name'],
                'rank': int(row['rank']),
                'count': int(row['count']),
                'prop100k': float(row['prop100k']),
                'pctwhite': float(row['pctwhite']) if row['pctwhite'] != '(S)' else 0,
                'pctblack': float(row['pctblack']) if row['pctblack'] != '(S)' else 0,
                'pctapi': float(row['pctapi']) if row['pctapi'] != '(S)' else 0,
                'pctaian': float(row['pctaian']) if row['pctaian'] != '(S)' else 0,
                'pct2prace': float(row['pct2prace']) if row['pct2prace'] != '(S)' else 0,
                'pcthispanic': float(row['pcthispanic']) if row['pcthispanic'] != '(S)' else 0,
            })
        except:
            pass

# Adler's exact metrics
ADLER = {
    'count': 16412,
    'rank': 2223,
    'prop100k': 5.56,
    'pctwhite': 94.9,
    'pctblack': 0.57,
    'pctapi': 0.71,
    'pctaian': 0.15,
    'pct2prace': 1.06,
    'pcthispanic': 2.61
}

def calculate_match_score(surname):
    """
    Calculate how closely a surname matches Adler across all metrics.
    Lower score = better match.
    """
    # Count difference (weight: high)
    count_diff = abs(surname['count'] - ADLER['count']) / ADLER['count'] * 100
    
    # Rank difference (weight: high)
    rank_diff = abs(surname['rank'] - ADLER['rank']) / ADLER['rank'] * 100
    
    # Proportion difference (weight: high)
    prop_diff = abs(surname['prop100k'] - ADLER['prop100k']) / ADLER['prop100k'] * 100
    
    # Demographic similarity (proxy for UK similarity - European origin names)
    # High white %, low Hispanic/Asian/Black = likely European origin
    demo_score = 0
    demo_score += abs(surname['pctwhite'] - ADLER['pctwhite'])
    demo_score += abs(surname['pctblack'] - ADLER['pctblack']) * 2  # Weight black diff more
    demo_score += abs(surname['pctapi'] - ADLER['pctapi']) * 2  # Weight asian diff more
    demo_score += abs(surname['pcthispanic'] - ADLER['pcthispanic']) * 2  # Weight hispanic diff more
    
    # Total weighted score
    total_score = (count_diff * 3) + (rank_diff * 3) + (prop_diff * 3) + demo_score
    
    return total_score

# Calculate match scores
for s in surnames:
    s['match_score'] = calculate_match_score(s)

# Sort by match score (best matches first)
surnames_sorted = sorted(surnames, key=lambda x: x['match_score'])

# Filter to European-origin names (high white %, low Hispanic/Asian)
# This is our proxy for "likely to have similar frequency in UK"
european_origin = [s for s in surnames_sorted 
                   if s['pctwhite'] > 85 
                   and s['pcthispanic'] < 10 
                   and s['pctapi'] < 5]

print("=" * 100)
print("ADLER STATISTICAL MATCH ANALYSIS")
print("=" * 100)
print(f"\nTARGET: ADLER")
print(f"  U.S. Count: {ADLER['count']:,}")
print(f"  U.S. Rank: {ADLER['rank']:,}")
print(f"  U.S. Proportion: {ADLER['prop100k']:.2f} per 100,000 ({ADLER['prop100k']/1000:.4f}%)")
print(f"  Demographics: {ADLER['pctwhite']:.1f}% White, {ADLER['pctblack']:.2f}% Black, {ADLER['pctapi']:.2f}% Asian, {ADLER['pcthispanic']:.2f}% Hispanic")
print(f"  UK Estimate: ~4 per 100,000 (~0.004%)")

print("\n" + "=" * 100)
print("TOP 50 SURNAMES MATCHING ADLER ACROSS ALL METRICS")
print("=" * 100)
print(f"\nCriteria: U.S. Count, U.S. Rank, U.S. Proportion, European Origin (proxy for UK similarity)")
print("-" * 100)

# Print header
print(f"{'#':<3} {'SURNAME':<15} {'RANK':<8} {'COUNT':<10} {'PROP/100K':<10} {'%WHITE':<8} {'%HISP':<8} {'%BLACK':<8} {'SCORE':<8}")
print("-" * 100)

# Print top 50 European-origin matches
for i, s in enumerate(european_origin[:50], 1):
    print(f"{i:<3} {s['name']:<15} {s['rank']:<8} {s['count']:<10,} {s['prop100k']:<10.2f} {s['pctwhite']:<8.1f} {s['pcthispanic']:<8.2f} {s['pctblack']:<8.2f} {s['match_score']:<8.1f}")

print("\n" + "=" * 100)
print("ANALYSIS OF BEST MATCHES")
print("=" * 100)

# Print detailed analysis of top 10
print("\nDETAILED COMPARISON - TOP 10 CLOSEST MATCHES:")
print("-" * 100)

for i, s in enumerate(european_origin[:10], 1):
    count_diff = abs(s['count'] - ADLER['count'])
    rank_diff = abs(s['rank'] - ADLER['rank'])
    prop_diff = abs(s['prop100k'] - ADLER['prop100k'])
    white_diff = abs(s['pctwhite'] - ADLER['pctwhite'])
    
    print(f"\n{i}. {s['name']}")
    print(f"   Count: {s['count']:,} (diff: {count_diff:+d} from Adler)")
    print(f"   Rank: {s['rank']:,} (diff: {rank_diff:+d} from Adler)")
    print(f"   Prop/100k: {s['prop100k']:.2f} (diff: {prop_diff:+.2f} from Adler)")
    print(f"   %White: {s['pctwhite']:.1f}% (diff: {white_diff:+.1f}% from Adler)")
    print(f"   %Hispanic: {s['pcthispanic']:.2f}%, %Black: {s['pctblack']:.2f}%, %Asian: {s['pctapi']:.2f}%")

# Find exact or near-exact matches
print("\n" + "=" * 100)
print("SURNAMES WITH NEARLY IDENTICAL STATISTICS TO ADLER")
print("(Within ±200 count AND ±50 rank AND similar demographics)")
print("=" * 100)

exact_matches = [s for s in european_origin 
                 if abs(s['count'] - ADLER['count']) <= 200 
                 and abs(s['rank'] - ADLER['rank']) <= 50]

for i, s in enumerate(exact_matches, 1):
    print(f"\n{i}. {s['name']}")
    print(f"   Count: {s['count']:,} | Rank: {s['rank']} | Prop: {s['prop100k']:.2f}/100k")
    print(f"   Demo: {s['pctwhite']:.1f}% White, {s['pcthispanic']:.2f}% Hispanic, {s['pctblack']:.2f}% Black")

# Summary statistics
print("\n" + "=" * 100)
print("SUMMARY: 4 METRICS MATCHING CRITERIA")
print("=" * 100)
print("""
For a surname to match ADLER across 4 metrics:
1. U.S. COUNT:  ~16,412 (tolerance: ±2,000 for "very close")
2. U.S. RANK:   ~2,223 (tolerance: ±200 for "very close")  
3. U.S. PROPORTION: ~5.56 per 100,000 (tolerance: ±0.5)
4. UK/EUROPEAN PROXY: >85% White, <10% Hispanic, <5% Asian
   (European-origin names more likely to have similar UK frequency)
""")
