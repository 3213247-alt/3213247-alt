#!/usr/bin/env python3
"""
Complete analysis of surnames matching Adler across all 4 metrics:
1. U.S. Census 2010 count (~16,412)
2. U.S. Census 2010 rank (~2,223)
3. U.S. proportion (0.0053%)
4. U.K. proportion (0.004%)
"""

import csv
import json

# Adler baseline metrics
ADLER = {
    'name': 'Adler',
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,
    'uk_proportion': 0.00004,  # 0.004% (unverified, from Wikipedia/Forebears)
}

US_POP_2010 = 308745538

def parse_census_file(filename):
    """Parse the Census CSV file"""
    surnames = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = row.get('name', '').strip()
                    count = int(row.get('count', 0))
                    rank = int(row.get('rank', 0))
                    if name and count > 0:
                        proportion = count / US_POP_2010
                        surnames.append({
                            'name': name,
                            'us_count': count,
                            'us_rank': rank,
                            'us_proportion': proportion,
                        })
                except (ValueError, KeyError):
                    continue
    except Exception as e:
        print(f"Error: {e}")
    return surnames

def calculate_full_match_score(surname_data, target=ADLER):
    """Calculate match score across all 4 metrics"""
    scores = []
    
    # US Count (25%)
    if surname_data.get('us_count'):
        count_diff = abs(surname_data['us_count'] - target['us_count'])
        count_score = max(0, 100 * (1 - min(count_diff / target['us_count'], 1.0)))
        scores.append(('us_count', count_score, 0.25))
    
    # US Rank (25%)
    if surname_data.get('us_rank'):
        rank_diff = abs(surname_data['us_rank'] - target['us_rank'])
        rank_score = max(0, 100 * (1 - min(rank_diff / target['us_rank'], 1.0)))
        scores.append(('us_rank', rank_score, 0.25))
    
    # US Proportion (25%)
    if surname_data.get('us_proportion'):
        prop_diff = abs(surname_data['us_proportion'] - target['us_proportion'])
        prop_score = max(0, 100 * (1 - min(prop_diff / target['us_proportion'], 1.0)))
        scores.append(('us_proportion', prop_score, 0.25))
    
    # UK Proportion (25%) - if available
    if surname_data.get('uk_proportion'):
        uk_diff = abs(surname_data['uk_proportion'] - target['uk_proportion'])
        uk_score = max(0, 100 * (1 - min(uk_diff / target['uk_proportion'], 1.0)))
        scores.append(('uk_proportion', uk_score, 0.25))
    else:
        # If UK data not available, only score on US metrics
        pass
    
    if not scores:
        return 0.0, {}
    
    total_score = sum(score * weight for _, score, weight in scores)
    metric_scores = {metric: score for metric, score, _ in scores}
    
    return total_score, metric_scores

def main():
    print("=" * 100)
    print("ADLER SURNAME METRIC MATCHING ANALYSIS")
    print("=" * 100)
    print()
    
    print("ADLER BASELINE METRICS:")
    print(f"  Name: {ADLER['name']}")
    print(f"  U.S. Count: {ADLER['us_count']:,}")
    print(f"  U.S. Rank: {ADLER['us_rank']:,}")
    print(f"  U.S. Proportion: {ADLER['us_proportion']:.6f} ({ADLER['us_proportion']*100:.4f}%)")
    print(f"  U.K. Proportion: {ADLER['uk_proportion']:.6f} ({ADLER['uk_proportion']*100:.4f}%) [Unverified]")
    print()
    
    # Load Census data
    census_file = '/tmp/census_data/Names_2010Census.csv'
    print(f"Loading U.S. Census 2010 data...")
    surnames = parse_census_file(census_file)
    print(f"Loaded {len(surnames):,} surnames")
    print()
    
    # Find surnames in rank range 2000-2500
    candidates = [s for s in surnames if 2000 <= s['us_rank'] <= 2500]
    print(f"Found {len(candidates)} surnames in rank range 2000-2500")
    print()
    
    # Score candidates on US metrics
    scored = []
    for s in candidates:
        score, metrics = calculate_full_match_score(s, ADLER)
        scored.append((s, score, metrics))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Display top 12
    print("=" * 100)
    print("TOP 12 SURNAMES MATCHING ADLER'S U.S. METRICS")
    print("=" * 100)
    print()
    
    top_12 = []
    for i, (surname, score, metrics) in enumerate(scored[:12], 1):
        top_12.append(surname['name'])
        print(f"{i:2d}. {surname['name']:20s}")
        print(f"    U.S. Count: {surname['us_count']:7,} (Adler: {ADLER['us_count']:,}) | Diff: {abs(surname['us_count'] - ADLER['us_count']):,}")
        print(f"    U.S. Rank:  {surname['us_rank']:7,} (Adler: {ADLER['us_rank']:,}) | Diff: {abs(surname['us_rank'] - ADLER['us_rank']):,}")
        print(f"    U.S. Prop:  {surname['us_proportion']*100:.4f}% (Adler: {ADLER['us_proportion']*100:.4f}%)")
        print(f"    Match Score: {score:.2f}/100")
        print()
    
    print("=" * 100)
    print("NEXT STEP: Cross-reference with U.K. surname data")
    print("=" * 100)
    print()
    print("To complete the 4-metric match, we need U.K. proportion data for:")
    for name in top_12:
        print(f"  - {name}")
    print()
    print("U.K. data sources to check:")
    print("  1. Office for National Statistics (ONS) surname data")
    print("  2. Forebears.io (aggregated, less reliable)")
    print("  3. Wikipedia surname frequency lists")
    print()
    
    return top_12

if __name__ == '__main__':
    main()
