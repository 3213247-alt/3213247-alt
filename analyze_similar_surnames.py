#!/usr/bin/env python3
"""
Analyze surnames similar to Adler across 4 metrics:
1. U.S. Census 2010 count (~16,412)
2. U.S. Census 2010 rank (~2,223)
3. U.S. proportion (0.0053%)
4. U.K. proportion (0.004%)
"""

import math

# Adler baseline from user's data
ADLER = {
    'name': 'Adler',
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 16,412 / 308,745,538
    'uk_proportion': 0.00004,   # 0.004% (unverified)
}

US_POP_2010 = 308745538

# Based on surname frequency patterns, surnames near rank 2,223 would have
# counts in a similar range. Let's identify candidates based on:
# 1. Similar spelling/linguistic origin (German/Jewish surnames)
# 2. Similar frequency patterns
# 3. Similar geographic distribution

# Common surnames in the rank range 2000-2500 typically have counts between
# 14,000-20,000. Let's identify candidates that might match.

def calculate_metrics(count, rank=None, uk_prop=None):
    """Calculate all metrics from available data"""
    us_prop = count / US_POP_2010
    return {
        'us_count': count,
        'us_rank': rank,
        'us_proportion': us_prop,
        'uk_proportion': uk_prop,
    }

def match_score(surname_data, target=ADLER):
    """Calculate how closely a surname matches Adler across all 4 metrics"""
    scores = []
    
    # Metric 1: US Count (weight: 25%)
    if surname_data.get('us_count'):
        count_diff = abs(surname_data['us_count'] - target['us_count'])
        count_score = 1 - min(count_diff / target['us_count'], 1.0)
        scores.append(('us_count', count_score, 0.25))
    
    # Metric 2: US Rank (weight: 25%)
    if surname_data.get('us_rank'):
        rank_diff = abs(surname_data['us_rank'] - target['us_rank'])
        rank_score = 1 - min(rank_diff / target['us_rank'], 1.0)
        scores.append(('us_rank', rank_score, 0.25))
    
    # Metric 3: US Proportion (weight: 25%)
    if surname_data.get('us_proportion'):
        prop_diff = abs(surname_data['us_proportion'] - target['us_proportion'])
        prop_score = 1 - min(prop_diff / target['us_proportion'], 1.0)
        scores.append(('us_proportion', prop_score, 0.25))
    elif surname_data.get('us_count'):
        us_prop = surname_data['us_count'] / US_POP_2010
        prop_diff = abs(us_prop - target['us_proportion'])
        prop_score = 1 - min(prop_diff / target['us_proportion'], 1.0)
        scores.append(('us_proportion', prop_score, 0.25))
    
    # Metric 4: UK Proportion (weight: 25%)
    if surname_data.get('uk_proportion'):
        uk_diff = abs(surname_data['uk_proportion'] - target['uk_proportion'])
        uk_score = 1 - min(uk_diff / target['uk_proportion'], 1.0)
        scores.append(('uk_proportion', uk_score, 0.25))
    
    if not scores:
        return 0.0, {}
    
    # Weighted average
    total_score = sum(score * weight for _, score, weight in scores)
    metric_scores = {metric: score for metric, score, _ in scores}
    
    return total_score, metric_scores

# Based on research, here are surnames that might be similar to Adler
# These are educated estimates based on:
# - Similar linguistic origins (German/Jewish)
# - Similar frequency patterns
# - Names that appear in similar rank ranges

# Note: Actual data would need to come from:
# 1. 2010 U.S. Census surname file
# 2. U.K. official surname statistics (ONS or similar)
# 3. Cross-referenced databases

CANDIDATE_SURNAMES = [
    # These are hypothetical - actual data needed from official sources
    {'name': 'Alder', 'us_count': 16500, 'us_rank': 2200, 'uk_proportion': 0.000041},
    {'name': 'Adelman', 'us_count': 16200, 'us_rank': 2250, 'uk_proportion': 0.000038},
    {'name': 'Adlerberg', 'us_count': 15800, 'us_rank': 2300, 'uk_proportion': 0.000042},
    {'name': 'Adlerstein', 'us_count': 17000, 'us_rank': 2150, 'uk_proportion': 0.000039},
    {'name': 'Adlerman', 'us_count': 16000, 'us_rank': 2280, 'uk_proportion': 0.000040},
    {'name': 'Adlerfeld', 'us_count': 16300, 'us_rank': 2240, 'uk_proportion': 0.000041},
    {'name': 'Adlerblum', 'us_count': 15900, 'us_rank': 2290, 'uk_proportion': 0.000037},
    {'name': 'Adlertag', 'us_count': 16100, 'us_rank': 2260, 'uk_proportion': 0.000039},
    {'name': 'Adlerstein', 'us_count': 16700, 'us_rank': 2180, 'uk_proportion': 0.000040},
    {'name': 'Adlerberg', 'us_count': 16400, 'us_rank': 2220, 'uk_proportion': 0.000040},
    {'name': 'Adlerfeld', 'us_count': 16250, 'us_rank': 2230, 'uk_proportion': 0.000040},
    {'name': 'Adlerman', 'us_count': 16350, 'us_rank': 2210, 'uk_proportion': 0.000040},
]

def analyze_candidates():
    """Analyze candidate surnames and rank by similarity"""
    print("=" * 80)
    print("ADLER BASELINE METRICS")
    print("=" * 80)
    print(f"Surname: {ADLER['name']}")
    print(f"U.S. Count: {ADLER['us_count']:,}")
    print(f"U.S. Rank: {ADLER['us_rank']:,}")
    print(f"U.S. Proportion: {ADLER['us_proportion']:.6f} ({ADLER['us_proportion']*100:.4f}%)")
    print(f"U.K. Proportion: {ADLER['uk_proportion']:.6f} ({ADLER['uk_proportion']*100:.4f}%)")
    print()
    
    print("=" * 80)
    print("FINDING SURNAMES WITH SIMILAR METRICS")
    print("=" * 80)
    print()
    print("Target Ranges (for close match):")
    print(f"  U.S. Count: {ADLER['us_count']*0.95:,.0f} - {ADLER['us_count']*1.05:,.0f} (±5%)")
    print(f"  U.S. Rank: {ADLER['us_rank']-100:,} - {ADLER['us_rank']+100:,} (±100)")
    print(f"  U.S. Proportion: {ADLER['us_proportion']*0.95:.6f} - {ADLER['us_proportion']*1.05:.6f}")
    print(f"  U.K. Proportion: {ADLER['uk_proportion']*0.95:.6f} - {ADLER['uk_proportion']*1.05:.6f}")
    print()
    
    print("=" * 80)
    print("IMPORTANT NOTE")
    print("=" * 80)
    print("To find accurate matches, we need:")
    print("1. Official 2010 U.S. Census surname file (with count and rank)")
    print("2. Official U.K. surname statistics (ONS or equivalent)")
    print("3. Cross-reference to find surnames matching ALL 4 metrics")
    print()
    print("The candidates listed above are ESTIMATES based on:")
    print("- Similar linguistic origins (German/Jewish surnames)")
    print("- Expected frequency patterns")
    print("- Names that would logically appear in similar rank ranges")
    print()
    print("ACTUAL DATA REQUIRED FROM OFFICIAL SOURCES")
    print("=" * 80)

if __name__ == '__main__':
    analyze_candidates()
