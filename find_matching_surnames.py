#!/usr/bin/env python3
"""
Find surnames matching Adler's metrics across 4 dimensions:
1. U.S. Census 2010 count (~16,412)
2. U.S. Census 2010 rank (~2,223)
3. U.S. proportion (0.0053%)
4. U.K. proportion (0.004%)
"""

import csv
import math

# Adler baseline metrics
ADLER = {
    'name': 'Adler',
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 16,412 / 308,745,538
    'uk_proportion': 0.00004,   # 0.004% (unverified)
}

US_POP_2010 = 308745538

def calculate_match_score(surname_data, target=ADLER):
    """
    Calculate how closely a surname matches Adler across all 4 metrics.
    Returns a score from 0-100, where 100 is perfect match.
    """
    scores = []
    weights = []
    
    # Metric 1: US Count (25% weight)
    if surname_data.get('us_count'):
        count_diff = abs(surname_data['us_count'] - target['us_count'])
        count_pct_diff = count_diff / target['us_count']
        # Score: 100 if exact match, decreases with difference
        count_score = max(0, 100 * (1 - min(count_pct_diff, 1.0)))
        scores.append(count_score)
        weights.append(0.25)
    
    # Metric 2: US Rank (25% weight)
    if surname_data.get('us_rank'):
        rank_diff = abs(surname_data['us_rank'] - target['us_rank'])
        rank_pct_diff = rank_diff / target['us_rank']
        rank_score = max(0, 100 * (1 - min(rank_pct_diff, 1.0)))
        scores.append(rank_score)
        weights.append(0.25)
    
    # Metric 3: US Proportion (25% weight)
    if surname_data.get('us_proportion'):
        prop_diff = abs(surname_data['us_proportion'] - target['us_proportion'])
        prop_pct_diff = prop_diff / target['us_proportion']
        prop_score = max(0, 100 * (1 - min(prop_pct_diff, 1.0)))
        scores.append(prop_score)
        weights.append(0.25)
    elif surname_data.get('us_count'):
        us_prop = surname_data['us_count'] / US_POP_2010
        prop_diff = abs(us_prop - target['us_proportion'])
        prop_pct_diff = prop_diff / target['us_proportion']
        prop_score = max(0, 100 * (1 - min(prop_pct_diff, 1.0)))
        scores.append(prop_score)
        weights.append(0.25)
    
    # Metric 4: UK Proportion (25% weight)
    if surname_data.get('uk_proportion'):
        uk_diff = abs(surname_data['uk_proportion'] - target['uk_proportion'])
        uk_pct_diff = uk_diff / target['uk_proportion']
        uk_score = max(0, 100 * (1 - min(uk_pct_diff, 1.0)))
        scores.append(uk_score)
        weights.append(0.25)
    
    if not scores:
        return 0.0
    
    # Weighted average
    total_weight = sum(weights)
    weighted_score = sum(s * w for s, w in zip(scores, weights)) / total_weight
    
    return weighted_score

def parse_census_file(filename):
    """Parse the Census CSV file and extract surname data"""
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
        print(f"Error reading file: {e}")
        return []
    
    return surnames

def find_matching_surnames():
    """Find surnames matching Adler's metrics"""
    
    print("=" * 80)
    print("ADLER BASELINE METRICS")
    print("=" * 80)
    print(f"Surname: {ADLER['name']}")
    print(f"U.S. Count: {ADLER['us_count']:,}")
    print(f"U.S. Rank: {ADLER['us_rank']:,}")
    print(f"U.S. Proportion: {ADLER['us_proportion']:.6f} ({ADLER['us_proportion']*100:.4f}%)")
    print(f"U.K. Proportion: {ADLER['uk_proportion']:.6f} ({ADLER['uk_proportion']*100:.4f}%)")
    print()
    
    # Parse Census data
    census_file = '/tmp/census_data/Names_2010Census.csv'
    print(f"Loading Census data from {census_file}...")
    surnames = parse_census_file(census_file)
    
    if not surnames:
        print("ERROR: Could not load Census data")
        return
    
    print(f"Loaded {len(surnames):,} surnames from Census data")
    print()
    
    # Find surnames in similar rank range (2000-2500)
    print("Searching for surnames with similar metrics...")
    print()
    
    # Filter to rank range 2000-2500 (around Adler's rank of 2223)
    candidates = [s for s in surnames if 2000 <= s['us_rank'] <= 2500]
    
    print(f"Found {len(candidates)} surnames in rank range 2000-2500")
    print()
    
    # Calculate match scores (using only US metrics for now)
    scored_candidates = []
    for surname in candidates:
        score = calculate_match_score(surname, ADLER)
        scored_candidates.append((surname, score))
    
    # Sort by match score (highest first)
    scored_candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Display top matches
    print("=" * 80)
    print("TOP 12 SURNAMES MATCHING ADLER'S U.S. METRICS")
    print("=" * 80)
    print()
    
    top_12 = scored_candidates[:12]
    
    for i, (surname, score) in enumerate(top_12, 1):
        print(f"{i:2d}. {surname['name']:20s} | Score: {score:5.2f}")
        print(f"    U.S. Count: {surname['us_count']:7,} | Rank: {surname['us_rank']:5,} | Prop: {surname['us_proportion']*100:.4f}%")
        print()
    
    print("=" * 80)
    print("NOTE: U.K. proportion data not available in Census file")
    print("Need to cross-reference with U.K. official surname statistics")
    print("=" * 80)
    
    return top_12

if __name__ == '__main__':
    find_matching_surnames()
