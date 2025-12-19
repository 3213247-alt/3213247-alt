#!/usr/bin/env python3
"""
Comprehensive analysis to find surnames matching Adler's statistics
across 4 metrics: US count, US rank, US proportion, and UK proportion
"""

import csv
import math
from typing import List, Dict, Tuple

# Adler's verified metrics from US Census 2010
ADLER_US_COUNT = 16412
ADLER_US_RANK = 2223
ADLER_US_PROP100K = 5.56  # per 100k population
ADLER_US_PROPORTION = 5.56 / 100000  # 0.0000556 = 0.00556%

# Target UK proportion (from user: 0.004% = 0.00004)
ADLER_UK_PROPORTION = 0.00004

# Tighter tolerance for very close matches
COUNT_TOLERANCE_STRICT = 0.10  # ±10%
RANK_TOLERANCE_STRICT = 0.10   # ±10%
PROP_TOLERANCE_STRICT = 0.15   # ±15%


def parse_us_census_csv(filename: str) -> List[Dict]:
    """Parse U.S. Census surname CSV file"""
    surnames = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = row.get('name', '').strip().upper()
                    count = int(row.get('count', 0))
                    rank = int(row.get('rank', 0))
                    prop100k = float(row.get('prop100k', 0))
                    proportion = prop100k / 100000
                    
                    surnames.append({
                        'name': name,
                        'count': count,
                        'rank': rank,
                        'prop100k': prop100k,
                        'proportion': proportion
                    })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"File {filename} not found")
    return surnames


def calculate_match_quality(surname: Dict) -> Dict:
    """Calculate how closely surname matches Adler's metrics"""
    count_diff_pct = abs(surname['count'] - ADLER_US_COUNT) / ADLER_US_COUNT
    rank_diff_pct = abs(surname['rank'] - ADLER_US_RANK) / ADLER_US_RANK
    prop_diff_pct = abs(surname['prop100k'] - ADLER_US_PROP100K) / ADLER_US_PROP100K
    
    # Overall match score (lower is better, 0 = perfect match)
    match_score = (count_diff_pct + rank_diff_pct + prop_diff_pct) / 3
    
    return {
        'count_diff_pct': count_diff_pct * 100,
        'rank_diff_pct': rank_diff_pct * 100,
        'prop_diff_pct': prop_diff_pct * 100,
        'match_score': match_score,
        'all_within_10pct': (count_diff_pct <= 0.10 and rank_diff_pct <= 0.10 and prop_diff_pct <= 0.10)
    }


def find_best_matches(us_surnames: List[Dict], max_results: int = 12) -> List[Tuple]:
    """Find surnames that match Adler's metrics very closely"""
    matches = []
    
    for surname in us_surnames:
        # Skip Adler itself
        if surname['name'] == 'ADLER':
            continue
            
        quality = calculate_match_quality(surname)
        
        # Include if all metrics within 10% tolerance
        if quality['all_within_10pct']:
            matches.append((surname, quality))
    
    # Sort by match score (best matches first)
    matches.sort(key=lambda x: x[1]['match_score'])
    
    return matches[:max_results]


def main():
    print("=" * 80)
    print("Finding Surnames Matching Adler's Statistics Across Multiple Metrics")
    print("=" * 80)
    print(f"\nAdler's Verified US Census 2010 Metrics:")
    print(f"  Count:      {ADLER_US_COUNT:,}")
    print(f"  Rank:       {ADLER_US_RANK:,}")
    print(f"  Per 100k:   {ADLER_US_PROP100K}")
    print(f"  Proportion: {ADLER_US_PROPORTION*100:.4f}%")
    print(f"\nTarget UK Proportion: {ADLER_UK_PROPORTION*100:.4f}%")
    print(f"\nSearching for surnames within ±10% on all US metrics...")
    
    # Load US Census data
    us_surnames = parse_us_census_csv("/workspace/Names_2010Census.csv")
    
    if not us_surnames:
        print("Error: Could not load US Census data")
        return
    
    print(f"Loaded {len(us_surnames):,} surnames from US Census 2010")
    
    # Find best matches
    matches = find_best_matches(us_surnames, max_results=12)
    
    print(f"\nFound {len(matches)} surnames matching all metrics within ±10%")
    print("\n" + "=" * 80)
    print("TOP 12 MATCHES (Very Close to Adler)")
    print("=" * 80)
    print(f"{'#':<4} {'Name':<18} {'Count':<12} {'Rank':<8} {'Per100k':<10} {'Count%':<10} {'Rank%':<10} {'Prop%':<10} {'Score':<8}")
    print("-" * 80)
    
    for i, (surname, quality) in enumerate(matches, 1):
        print(f"{i:<4} {surname['name']:<18} {surname['count']:<12,} {surname['rank']:<8,} "
              f"{surname['prop100k']:<10.2f} {quality['count_diff_pct']:<10.2f} "
              f"{quality['rank_diff_pct']:<10.2f} {quality['prop_diff_pct']:<10.2f} "
              f"{quality['match_score']*100:<8.2f}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS NOTES:")
    print("=" * 80)
    print("• Count% = Percentage difference from Adler's count")
    print("• Rank% = Percentage difference from Adler's rank")
    print("• Prop% = Percentage difference from Adler's proportion")
    print("• Score = Average percentage difference (lower is better)")
    print("\n• UK proportion data would need to be verified separately")
    print("  from official UK statistical sources (ONS, etc.)")
    
    # Show the best single match
    if matches:
        best = matches[0]
        print(f"\n{'='*80}")
        print(f"BEST MATCH: {best[0]['name']}")
        print(f"{'='*80}")
        print(f"US Count:      {best[0]['count']:,} (vs Adler: {ADLER_US_COUNT:,}, diff: {best[1]['count_diff_pct']:.2f}%)")
        print(f"US Rank:       {best[0]['rank']:,} (vs Adler: {ADLER_US_RANK:,}, diff: {best[1]['rank_diff_pct']:.2f}%)")
        print(f"US Per 100k:   {best[0]['prop100k']:.2f} (vs Adler: {ADLER_US_PROP100K:.2f}, diff: {best[1]['prop_diff_pct']:.2f}%)")
        print(f"Overall Score: {best[1]['match_score']*100:.2f}% average difference")


if __name__ == "__main__":
    main()
