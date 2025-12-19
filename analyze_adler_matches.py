#!/usr/bin/env python3
"""
Analyze US Census 2010 surname data to find surnames matching Adler across 4 metrics
"""

import csv
import json
from typing import List, Dict, Tuple

# Adler baseline metrics (verified from census)
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 16412 / 308745538,  # 0.00005312
    'prop100k': 5.56,  # per 100k
}

US_POPULATION_2010 = 308745538

def load_census_data(filename: str) -> List[Dict]:
    """Load census surname data"""
    surnames = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                surname = row['name'].strip()
                rank = int(row['rank'])
                count = int(row['count'])
                prop100k = float(row['prop100k'])
                
                surnames.append({
                    'surname': surname,
                    'us_count': count,
                    'us_rank': rank,
                    'us_proportion': count / US_POPULATION_2010,
                    'prop100k': prop100k
                })
            except (ValueError, KeyError) as e:
                continue
    return surnames

def calculate_match_score(surname_data: Dict, adler_metrics: Dict) -> Tuple[float, Dict]:
    """
    Calculate similarity score (0-100, higher = more similar)
    """
    details = {}
    scores = []
    
    # Metric 1: US Count similarity
    count_diff = abs(surname_data['us_count'] - adler_metrics['us_count'])
    count_ratio = count_diff / adler_metrics['us_count']
    count_score = max(0, (1 - min(count_ratio, 1.0)) * 100)
    scores.append(count_score)
    details['count_score'] = count_score
    details['count_diff_pct'] = count_ratio * 100
    
    # Metric 2: US Rank similarity
    rank_diff = abs(surname_data['us_rank'] - adler_metrics['us_rank'])
    rank_ratio = rank_diff / adler_metrics['us_rank']
    rank_score = max(0, (1 - min(rank_ratio, 1.0)) * 100)
    scores.append(rank_score)
    details['rank_score'] = rank_score
    details['rank_diff_pct'] = rank_ratio * 100
    
    # Metric 3: US Proportion similarity
    prop_diff = abs(surname_data['us_proportion'] - adler_metrics['us_proportion'])
    prop_ratio = prop_diff / adler_metrics['us_proportion']
    prop_score = max(0, (1 - min(prop_ratio, 1.0)) * 100)
    scores.append(prop_score)
    details['prop_score'] = prop_score
    details['prop_diff_pct'] = prop_ratio * 100
    
    # Metric 4: prop100k similarity (alternative proportion measure)
    prop100k_diff = abs(surname_data['prop100k'] - adler_metrics['prop100k'])
    prop100k_ratio = prop100k_diff / adler_metrics['prop100k']
    prop100k_score = max(0, (1 - min(prop100k_ratio, 1.0)) * 100)
    scores.append(prop100k_score)
    details['prop100k_score'] = prop100k_score
    details['prop100k_diff_pct'] = prop100k_ratio * 100
    
    # Average score across all 4 metrics
    avg_score = sum(scores) / len(scores)
    details['avg_score'] = avg_score
    details['metrics_matched'] = len(scores)
    
    return avg_score, details

def find_matching_surnames(surnames: List[Dict], adler_metrics: Dict,
                          count_range: Tuple[int, int] = (13000, 20000),
                          rank_range: Tuple[int, int] = (1700, 2700),
                          top_n: int = 50) -> List[Tuple[str, float, Dict, Dict]]:
    """Find surnames matching Adler's metrics"""
    matches = []
    
    for surname_data in surnames:
        surname = surname_data.get('surname', '')
        if not surname:
            continue
        
        # Filter by count and rank ranges
        us_count = surname_data.get('us_count', 0)
        us_rank = surname_data.get('us_rank', 0)
        
        if not (count_range[0] <= us_count <= count_range[1]):
            continue
        if not (rank_range[0] <= us_rank <= rank_range[1]):
            continue
        
        # Calculate match score
        score, details = calculate_match_score(surname_data, adler_metrics)
        
        matches.append((surname, score, surname_data, details))
    
    # Sort by match score (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches[:top_n]

def print_results(matches: List[Tuple[str, float, Dict, Dict]]):
    """Print formatted results"""
    print("\n" + "=" * 120)
    print("ADLER SURNAME MATCHING RESULTS - Top 50 Matches Across 4 Metrics")
    print("=" * 120)
    print(f"\nAdler Baseline Metrics:")
    print(f"  US Count: {ADLER_METRICS['us_count']:,}")
    print(f"  US Rank: {ADLER_METRICS['us_rank']:,}")
    print(f"  US Proportion: {ADLER_METRICS['us_proportion']*100:.5f}%")
    print(f"  Prop per 100k: {ADLER_METRICS['prop100k']:.2f}")
    
    print("\n" + "-" * 120)
    print(f"{'Rank':<6} {'Surname':<20} {'US Count':<12} {'US Rank':<10} {'US Prop %':<12} {'Prop/100k':<12} {'Match Score':<12}")
    print("-" * 120)
    
    for i, (surname, score, data, details) in enumerate(matches, 1):
        us_count = data.get('us_count', 0)
        us_rank = data.get('us_rank', 0)
        us_prop = data.get('us_proportion', 0) * 100
        prop100k = data.get('prop100k', 0)
        
        print(f"{i:<6} {surname:<20} {us_count:<12,} {us_rank:<10,} {us_prop:<12.5f} {prop100k:<12.2f} {score:<12.2f}%")
    
    print("\n" + "=" * 120)
    print("BEST MATCH (highest score across all 4 metrics simultaneously):")
    if matches:
        best = matches[0]
        print(f"  Surname: {best[0]}")
        print(f"  Overall Match Score: {best[1]:.2f}%")
        print(f"  US Count: {best[2]['us_count']:,} (Adler: {ADLER_METRICS['us_count']:,}, diff: {abs(best[2]['us_count'] - ADLER_METRICS['us_count']):,})")
        print(f"  US Rank: {best[2]['us_rank']:,} (Adler: {ADLER_METRICS['us_rank']:,}, diff: {abs(best[2]['us_rank'] - ADLER_METRICS['us_rank']):,})")
        print(f"  US Proportion: {best[2]['us_proportion']*100:.5f}% (Adler: {ADLER_METRICS['us_proportion']*100:.5f}%)")
        print(f"  Prop per 100k: {best[2]['prop100k']:.2f} (Adler: {ADLER_METRICS['prop100k']:.2f})")
        print(f"\n  Individual Metric Scores:")
        print(f"    Count Score: {best[3]['count_score']:.2f}%")
        print(f"    Rank Score: {best[3]['rank_score']:.2f}%")
        print(f"    Proportion Score: {best[3]['prop_score']:.2f}%")
        print(f"    Prop100k Score: {best[3]['prop100k_score']:.2f}%")

if __name__ == '__main__':
    print("Loading US Census 2010 surname data...")
    surnames = load_census_data('Names_2010Census.csv')
    print(f"Loaded {len(surnames):,} surnames")
    
    # Verify Adler data
    adler_data = [s for s in surnames if s['surname'].upper() == 'ADLER']
    if adler_data:
        print(f"\nVerified Adler in data:")
        print(f"  Count: {adler_data[0]['us_count']:,}")
        print(f"  Rank: {adler_data[0]['us_rank']:,}")
    
    print("\nFinding surnames matching Adler across 4 metrics...")
    print("  Count range: 13,000 - 20,000")
    print("  Rank range: 1,700 - 2,700")
    
    matches = find_matching_surnames(surnames, ADLER_METRICS)
    print(f"\nFound {len(matches)} matching surnames")
    
    print_results(matches)
    
    # Save results to JSON
    results = []
    for surname, score, data, details in matches:
        results.append({
            'surname': surname,
            'match_score': score,
            'us_count': data['us_count'],
            'us_rank': data['us_rank'],
            'us_proportion': data['us_proportion'],
            'prop100k': data['prop100k'],
            'score_details': details
        })
    
    with open('adler_matches_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to adler_matches_results.json")
