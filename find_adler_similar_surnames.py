#!/usr/bin/env python3
"""
Find surnames similar to Adler across multiple metrics:
- U.S. Census 2010: count = 16,412, rank = 2,223, proportion = 0.0053%
- U.K. proportion = 0.004% (unverified)
"""

# Adler baseline metrics
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 0.0053%
    'uk_proportion': 0.00004,   # 0.004% (unverified)
}

US_POPULATION_2010 = 308745538

def calculate_proportion(count, population=US_POPULATION_2010):
    """Calculate proportion from count"""
    return count / population

def calculate_count_from_proportion(proportion, population=US_POPULATION_2010):
    """Calculate count from proportion"""
    return int(proportion * population)

def similarity_score(surname_metrics, adler_metrics=ADLER_METRICS):
    """
    Calculate similarity score (lower is better, 0 = perfect match)
    Uses normalized differences across all metrics
    """
    scores = []
    
    # US count similarity (within ±10% = good match)
    if 'us_count' in surname_metrics:
        count_diff = abs(surname_metrics['us_count'] - adler_metrics['us_count'])
        count_score = count_diff / adler_metrics['us_count']  # normalized difference
        scores.append(count_score)
    
    # US rank similarity (within ±200 ranks = good match)
    if 'us_rank' in surname_metrics:
        rank_diff = abs(surname_metrics['us_rank'] - adler_metrics['us_rank'])
        rank_score = rank_diff / adler_metrics['us_rank']  # normalized difference
        scores.append(rank_score)
    
    # US proportion similarity
    if 'us_proportion' in surname_metrics:
        prop_diff = abs(surname_metrics['us_proportion'] - adler_metrics['us_proportion'])
        prop_score = prop_diff / adler_metrics['us_proportion']
        scores.append(prop_score)
    elif 'us_count' in surname_metrics:
        # Calculate proportion from count
        prop = calculate_proportion(surname_metrics['us_count'])
        prop_diff = abs(prop - adler_metrics['us_proportion'])
        prop_score = prop_diff / adler_metrics['us_proportion']
        scores.append(prop_score)
    
    # UK proportion similarity
    if 'uk_proportion' in surname_metrics:
        uk_diff = abs(surname_metrics['uk_proportion'] - adler_metrics['uk_proportion'])
        uk_score = uk_diff / adler_metrics['uk_proportion']
        scores.append(uk_score)
    
    if not scores:
        return float('inf')
    
    return sum(scores) / len(scores)  # Average normalized difference

def find_similar_surnames():
    """
    Find surnames with similar metrics to Adler.
    This function will need actual data sources.
    For now, it provides the framework.
    """
    
    # Candidate surnames to check (common German/Jewish surnames similar to Adler)
    # These are educated guesses based on similar origins and likely similar frequencies
    candidates = [
        # Similar German/Jewish surnames
        {'name': 'Adler', 'us_count': 16412, 'us_rank': 2223, 'us_proportion': 0.000053, 'uk_proportion': 0.00004},
        {'name': 'Alder', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerstein', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adelman', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerberg', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerstein', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerblum', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerman', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlertag', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerfeld', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerstein', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
        {'name': 'Adlerberg', 'us_count': None, 'us_rank': None, 'us_proportion': None, 'uk_proportion': None},
    ]
    
    print("Adler Baseline Metrics:")
    print(f"  U.S. Count: {ADLER_METRICS['us_count']:,}")
    print(f"  U.S. Rank: {ADLER_METRICS['us_rank']:,}")
    print(f"  U.S. Proportion: {ADLER_METRICS['us_proportion']:.6f} ({ADLER_METRICS['us_proportion']*100:.4f}%)")
    print(f"  U.K. Proportion: {ADLER_METRICS['uk_proportion']:.6f} ({ADLER_METRICS['uk_proportion']*100:.4f}%)")
    print()
    
    print("To find matching surnames, we need:")
    print("1. 2010 U.S. Census surname data (count and rank)")
    print("2. U.K. surname frequency data")
    print("3. Cross-reference to find surnames matching all metrics")
    print()
    
    print("Target ranges for matching surnames:")
    print(f"  U.S. Count: {ADLER_METRICS['us_count']*0.9:,.0f} - {ADLER_METRICS['us_count']*1.1:,.0f} (±10%)")
    print(f"  U.S. Rank: {ADLER_METRICS['us_rank']-200:,} - {ADLER_METRICS['us_rank']+200:,} (±200)")
    print(f"  U.S. Proportion: {ADLER_METRICS['us_proportion']*0.9:.6f} - {ADLER_METRICS['us_proportion']*1.1:.6f}")
    print(f"  U.K. Proportion: {ADLER_METRICS['uk_proportion']*0.9:.6f} - {ADLER_METRICS['uk_proportion']*1.1:.6f}")
    
    return candidates

if __name__ == '__main__':
    find_similar_surnames()
