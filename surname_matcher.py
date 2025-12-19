#!/usr/bin/env python3
"""
Find surnames matching Adler's demographic statistics across multiple metrics.
"""

import csv
import math
from typing import List, Dict, Tuple

# Target metrics for ADLER
TARGET_RANK = 2223
TARGET_COUNT = 16412
TARGET_PROP100K = 5.56  # per 100,000
TARGET_US_PERCENT = 0.00556  # 5.56 per 100k = 0.00556%

# For UK, 0.004% target (unverified but used as constraint)
TARGET_UK_PERCENT = 0.004


def calculate_distance(surname_data: Dict, weights: Dict[str, float]) -> float:
    """
    Calculate weighted distance from target metrics.
    Lower distance = closer match.
    """
    rank_diff = abs(surname_data['rank'] - TARGET_RANK) / TARGET_RANK
    count_diff = abs(surname_data['count'] - TARGET_COUNT) / TARGET_COUNT
    prop_diff = abs(surname_data['prop100k'] - TARGET_PROP100K) / TARGET_PROP100K
    
    # Combined metric: weighted sum of normalized differences
    distance = (
        weights['rank'] * rank_diff +
        weights['count'] * count_diff +
        weights['prop'] * prop_diff
    )
    
    return distance


def load_census_data(filepath: str) -> List[Dict]:
    """Load and parse census surname data."""
    surnames = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
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
                })
            except (ValueError, KeyError):
                continue
    
    return surnames


def find_closest_matches(surnames: List[Dict], n: int = 50) -> List[Tuple[Dict, float]]:
    """Find n surnames with closest metrics to Adler."""
    
    # Equal weighting across all three metrics
    weights = {
        'rank': 1.0,
        'count': 1.0,
        'prop': 1.0,
    }
    
    # Calculate distances for all surnames
    matches = []
    for surname in surnames:
        # Skip Adler itself
        if surname['name'] == 'ADLER':
            continue
            
        distance = calculate_distance(surname, weights)
        matches.append((surname, distance))
    
    # Sort by distance and return top n
    matches.sort(key=lambda x: x[1])
    return matches[:n]


def main():
    print("=" * 80)
    print("SURNAME MATCHING ANALYSIS: Finding surnames similar to ADLER")
    print("=" * 80)
    print()
    
    # Load census data
    print("Loading 2010 U.S. Census surname data...")
    surnames = load_census_data('/tmp/Names_2010Census.csv')
    print(f"Loaded {len(surnames):,} surnames")
    print()
    
    # Find Adler for reference
    adler = [s for s in surnames if s['name'] == 'ADLER'][0]
    print("TARGET: ADLER Statistics")
    print("-" * 80)
    print(f"  Rank:           {adler['rank']:,}")
    print(f"  Count:          {adler['count']:,}")
    print(f"  Per 100k:       {adler['prop100k']}")
    print(f"  U.S. Percent:   {adler['prop100k']/1000:.5f}% (= {adler['prop100k']}/1000)")
    print(f"  Target UK%%:     0.004% (unverified)")
    print()
    
    # Find closest matches
    print("Finding 50 closest matches...")
    print()
    matches = find_closest_matches(surnames, n=50)
    
    print("=" * 80)
    print("TOP 50 SURNAMES WITH CLOSEST MATCHING METRICS TO ADLER")
    print("=" * 80)
    print()
    print(f"{'#':<4} {'SURNAME':<20} {'RANK':<8} {'COUNT':<10} {'PER 100K':<10} {'US %':<10} {'DISTANCE':<10}")
    print("-" * 80)
    
    for i, (surname, distance) in enumerate(matches, 1):
        us_percent = surname['prop100k'] / 1000
        print(f"{i:<4} {surname['name']:<20} {surname['rank']:<8,} {surname['count']:<10,} "
              f"{surname['prop100k']:<10.2f} {us_percent:<10.5f}% {distance:<10.4f}")
    
    print()
    print("=" * 80)
    print("CLOSEST MATCH DETAILS")
    print("=" * 80)
    
    best_match = matches[0][0]
    best_distance = matches[0][1]
    
    print()
    print(f"BEST MATCH: {best_match['name']}")
    print("-" * 80)
    print(f"  Rank:           {best_match['rank']:,} (target: {TARGET_RANK:,}, diff: {abs(best_match['rank']-TARGET_RANK):,})")
    print(f"  Count:          {best_match['count']:,} (target: {TARGET_COUNT:,}, diff: {abs(best_match['count']-TARGET_COUNT):,})")
    print(f"  Per 100k:       {best_match['prop100k']} (target: {TARGET_PROP100K}, diff: {abs(best_match['prop100k']-TARGET_PROP100K):.2f})")
    print(f"  U.S. Percent:   {best_match['prop100k']/1000:.5f}% (target: {TARGET_US_PERCENT:.5f}%)")
    print(f"  Distance Score: {best_distance:.6f} (lower = better match)")
    print()
    
    # Show comparison
    print("METRIC COMPARISON:")
    print("-" * 80)
    print(f"{'Metric':<20} {'ADLER':<20} {best_match['name']:<20} {'% Difference':<15}")
    print("-" * 80)
    
    rank_pct = (best_match['rank'] - adler['rank']) / adler['rank'] * 100
    count_pct = (best_match['count'] - adler['count']) / adler['count'] * 100
    prop_pct = (best_match['prop100k'] - adler['prop100k']) / adler['prop100k'] * 100
    
    print(f"{'Rank':<20} {adler['rank']:<20,} {best_match['rank']:<20,} {rank_pct:>+.2f}%")
    print(f"{'Count':<20} {adler['count']:<20,} {best_match['count']:<20,} {count_pct:>+.2f}%")
    print(f"{'Per 100k':<20} {adler['prop100k']:<20.2f} {best_match['prop100k']:<20.2f} {prop_pct:>+.2f}%")
    print()
    
    # Export results
    print("Exporting results to surname_matches.csv...")
    with open('/workspace/surname_matches.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank_Match', 'Surname', 'Census_Rank', 'Count', 'Per_100k', 'US_Percent', 'Distance_Score'])
        for i, (surname, distance) in enumerate(matches, 1):
            us_percent = surname['prop100k'] / 1000
            writer.writerow([i, surname['name'], surname['rank'], surname['count'], 
                           surname['prop100k'], f"{us_percent:.5f}%", f"{distance:.6f}"])
    
    print("✓ Results saved to surname_matches.csv")
    print()


if __name__ == '__main__':
    main()
