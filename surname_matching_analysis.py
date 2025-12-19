#!/usr/bin/env python3
"""
Surname Matching Analysis: Find surnames that match Adler closely across 4 metrics
Metrics:
1. US Count (Adler: 16,412)
2. US Rank (Adler: 2,223)
3. US Proportion (Adler: 0.0053% = 16,412 / 308,745,538)
4. UK Proportion (Adler: ~0.004% - unverified)
"""

import json
import math
from typing import List, Dict, Tuple

# Adler baseline metrics
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 0.0053% as decimal
    'uk_proportion': 0.00004,   # 0.004% as decimal (unverified)
}

US_POPULATION_2010 = 308745538

def calculate_similarity_score(surname_data: Dict, adler_metrics: Dict) -> float:
    """
    Calculate similarity score across all 4 metrics.
    Lower score = more similar (using normalized distance)
    """
    scores = []
    
    # Metric 1: US Count similarity (within 20% range)
    if 'us_count' in surname_data:
        count_diff = abs(surname_data['us_count'] - adler_metrics['us_count'])
        count_ratio = count_diff / adler_metrics['us_count']
        scores.append(count_ratio)
    
    # Metric 2: US Rank similarity (within 20% range)
    if 'us_rank' in surname_data:
        rank_diff = abs(surname_data['us_rank'] - adler_metrics['us_rank'])
        rank_ratio = rank_diff / adler_metrics['us_rank']
        scores.append(rank_ratio)
    
    # Metric 3: US Proportion similarity
    if 'us_count' in surname_data:
        us_prop = surname_data['us_count'] / US_POPULATION_2010
        prop_diff = abs(us_prop - adler_metrics['us_proportion'])
        prop_ratio = prop_diff / adler_metrics['us_proportion']
        scores.append(prop_ratio)
    
    # Metric 4: UK Proportion similarity
    if 'uk_proportion' in surname_data:
        uk_prop_diff = abs(surname_data['uk_proportion'] - adler_metrics['uk_proportion'])
        uk_prop_ratio = uk_prop_diff / adler_metrics['uk_proportion']
        scores.append(uk_prop_ratio)
    
    # Return average similarity score (lower is better)
    if scores:
        return sum(scores) / len(scores)
    return float('inf')

def find_matching_surnames(surname_database: List[Dict], adler_metrics: Dict, 
                          max_results: int = 50) -> List[Tuple[str, float, Dict]]:
    """
    Find surnames matching Adler metrics closely.
    Returns list of (surname, similarity_score, metrics) tuples, sorted by similarity.
    """
    matches = []
    
    for surname_data in surname_database:
        surname = surname_data.get('surname', '')
        if not surname:
            continue
        
        score = calculate_similarity_score(surname_data, adler_metrics)
        
        # Only include if we have at least 3 of 4 metrics
        metric_count = sum([
            'us_count' in surname_data,
            'us_rank' in surname_data,
            'uk_proportion' in surname_data
        ])
        
        if metric_count >= 3:
            matches.append((surname, score, surname_data))
    
    # Sort by similarity score (lowest = most similar)
    matches.sort(key=lambda x: x[1])
    
    return matches[:max_results]

def generate_surname_candidates() -> List[Dict]:
    """
    Generate candidate surnames based on known patterns.
    This would ideally use actual census data, but we'll create
    a representative sample based on Adler's characteristics.
    """
    candidates = []
    
    # Surnames with similar characteristics to Adler:
    # - German/Jewish origin
    # - 5 letters
    # - Similar frequency patterns
    
    # These are example candidates - in reality, we'd query actual census data
    # For now, creating a framework that can work with real data
    
    sample_surnames = [
        {'surname': 'Adler', 'us_count': 16412, 'us_rank': 2223, 'uk_proportion': 0.00004},
        # Add more candidates here - this would come from actual census data
    ]
    
    return sample_surnames

if __name__ == '__main__':
    print("Surname Matching Analysis: Finding surnames similar to Adler")
    print("=" * 60)
    print(f"\nAdler Baseline Metrics:")
    print(f"  US Count: {ADLER_METRICS['us_count']:,}")
    print(f"  US Rank: {ADLER_METRICS['us_rank']:,}")
    print(f"  US Proportion: {ADLER_METRICS['us_proportion']*100:.4f}%")
    print(f"  UK Proportion: {ADLER_METRICS['uk_proportion']*100:.4f}%")
    print("\n" + "=" * 60)
    
    # Note: This script provides the framework
    # Actual surname data would need to be loaded from census files
    print("\nNote: This script provides the analysis framework.")
    print("To use with real data, load surname databases with:")
    print("  - US Census 2010 surname file")
    print("  - UK surname statistics")
    print("  - Both count and rank data")
