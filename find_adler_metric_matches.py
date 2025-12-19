#!/usr/bin/env python3
"""
Find surnames matching Adler across 4 metrics:
1. U.S. Census 2010: count ~16,412, rank ~2,223, proportion ~0.0053%
2. U.K. proportion ~0.004% (unverified)
3. Linguistic similarity (German/Jewish origin, similar spelling)
4. Demographic/geographic distribution similarity

This script uses actual U.S. Census 2010 data to find exact metric matches.
"""

import csv
import json
import re
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher
import math

# Adler baseline metrics (from U.S. Census 2010)
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 0.0053% (user corrected)
    'us_prop100k': 5.56,  # per 100k from census
    'uk_proportion': 0.00004,   # 0.004% (unverified)
    'origin': 'German/Jewish',
    'length': 5,
    'pattern': 'A-d-l-e-r',  # Consonant-vowel-consonant-vowel-consonant
}

# Tolerance ranges for matching (percentage of Adler's value)
TOLERANCE = {
    'count': 0.30,      # ±30% of count (11,488 to 21,336)
    'rank': 0.30,       # ±30% of rank (1,556 to 2,890)
    'proportion': 0.30, # ±30% of proportion
    'prop100k': 0.30,   # ±30% of prop100k
}

def similarity_score(s1: str, s2: str) -> float:
    """Calculate string similarity using SequenceMatcher"""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def phonetic_similarity(s1: str, s2: str) -> float:
    """Check if surnames sound similar (consonant pattern matching)"""
    def get_consonants(s):
        return ''.join(c for c in s.lower() if c not in 'aeiou')
    
    c1 = get_consonants(s1)
    c2 = get_consonants(s2)
    
    if len(c1) == 0 or len(c2) == 0:
        return 0.0
    
    return similarity_score(c1, c2)

def pattern_match(surname: str) -> bool:
    """Check if surname matches Adler's pattern (C-V-C-V-C)"""
    pattern = re.compile(r'^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]', re.IGNORECASE)
    return bool(pattern.match(surname))

def is_german_jewish_origin(surname: str) -> bool:
    """Heuristic check for German/Jewish origin surnames"""
    # Common German/Jewish surname patterns and endings
    german_jewish_patterns = [
        r'.*berg$', r'.*stein$', r'.*man$', r'.*mann$', r'.*feld$',
        r'.*bach$', r'.*heim$', r'.*witz$', r'.*son$', r'.*sen$',
        r'^[A-Z][aeiou][bcdfghjklmnpqrstvwxyz]',  # Pattern like Adler
    ]
    
    surname_lower = surname.lower()
    for pattern in german_jewish_patterns:
        if re.match(pattern, surname_lower):
            return True
    
    # Common German/Jewish surnames
    common_names = ['adler', 'meyer', 'mayer', 'cohen', 'levy', 'levin', 
                    'goldberg', 'rosenberg', 'friedman', 'schwartz', 'weiss',
                    'kahn', 'katz', 'stein', 'berg', 'baum', 'blum', 'roth']
    
    return surname_lower in common_names

def load_census_data(csv_file: str) -> Dict[str, Dict]:
    """Load U.S. Census 2010 surname data"""
    census_data = {}
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            surname = row['name'].upper().strip()
            try:
                census_data[surname] = {
                    'rank': int(row['rank']),
                    'count': int(row['count']),
                    'prop100k': float(row['prop100k']),
                    'proportion': float(row['prop100k']) / 100000.0,  # Convert to proportion
                    'pctwhite': float(row.get('pctwhite', 0)),
                    'pctblack': float(row.get('pctblack', 0)),
                    'pctapi': float(row.get('pctapi', 0)),
                    'pcthispanic': float(row.get('pcthispanic', 0)),
                }
            except (ValueError, KeyError) as e:
                continue
    
    return census_data

def calculate_metric_match_score(surname_data: Dict, adler_data: Dict) -> Dict[str, float]:
    """Calculate how closely surname matches Adler's metrics"""
    scores = {}
    
    # Count match (closer is better)
    count_diff = abs(surname_data['count'] - adler_data['us_count'])
    count_max_diff = adler_data['us_count'] * TOLERANCE['count']
    scores['count_match'] = max(0, 1.0 - (count_diff / count_max_diff)) if count_max_diff > 0 else 0.0
    
    # Rank match (closer is better)
    rank_diff = abs(surname_data['rank'] - adler_data['us_rank'])
    rank_max_diff = adler_data['us_rank'] * TOLERANCE['rank']
    scores['rank_match'] = max(0, 1.0 - (rank_diff / rank_max_diff)) if rank_max_diff > 0 else 0.0
    
    # Proportion match (closer is better)
    prop_diff = abs(surname_data['proportion'] - adler_data['us_proportion'])
    prop_max_diff = adler_data['us_proportion'] * TOLERANCE['proportion']
    scores['proportion_match'] = max(0, 1.0 - (prop_diff / prop_max_diff)) if prop_max_diff > 0 else 0.0
    
    # Prop100k match
    prop100k_diff = abs(surname_data['prop100k'] - adler_data['us_prop100k'])
    prop100k_max_diff = adler_data['us_prop100k'] * TOLERANCE['prop100k']
    scores['prop100k_match'] = max(0, 1.0 - (prop100k_diff / prop100k_max_diff)) if prop100k_max_diff > 0 else 0.0
    
    # Demographic distribution similarity (using pctwhite as proxy)
    demo_diff = abs(surname_data['pctwhite'] - adler_data.get('pctwhite', 94.9))
    scores['demographic_match'] = max(0, 1.0 - (demo_diff / 100.0))
    
    return scores

def find_metric_matches(census_data: Dict[str, Dict], adler_metrics: Dict) -> List[Dict]:
    """Find surnames matching Adler's demographic metrics"""
    matches = []
    
    # Calculate tolerance ranges
    count_min = adler_metrics['us_count'] * (1 - TOLERANCE['count'])
    count_max = adler_metrics['us_count'] * (1 + TOLERANCE['count'])
    rank_min = int(adler_metrics['us_rank'] * (1 - TOLERANCE['rank']))
    rank_max = int(adler_metrics['us_rank'] * (1 + TOLERANCE['rank']))
    prop_min = adler_metrics['us_proportion'] * (1 - TOLERANCE['proportion'])
    prop_max = adler_metrics['us_proportion'] * (1 + TOLERANCE['proportion'])
    
    print(f"Searching for surnames with:")
    print(f"  Count: {count_min:,.0f} to {count_max:,.0f}")
    print(f"  Rank: {rank_min:,} to {rank_max:,}")
    print(f"  Proportion: {prop_min:.6f} to {prop_max:.6f}")
    print()
    
    for surname, data in census_data.items():
        if surname == 'ADLER':
            continue
        
        # Check if within tolerance ranges
        if (count_min <= data['count'] <= count_max and
            rank_min <= data['rank'] <= rank_max and
            prop_min <= data['proportion'] <= prop_max):
            
            # Calculate metric match scores
            metric_scores = calculate_metric_match_score(data, {
                'us_count': adler_metrics['us_count'],
                'us_rank': adler_metrics['us_rank'],
                'us_proportion': adler_metrics['us_proportion'],
                'us_prop100k': adler_metrics['us_prop100k'],
                'pctwhite': census_data.get('ADLER', {}).get('pctwhite', 94.9),  # Adler's pctwhite from census
            })
            
            # Calculate linguistic similarity
            spelling_sim = similarity_score('ADLER', surname)
            phonetic_sim = phonetic_similarity('ADLER', surname)
            pattern_match_score = 1.0 if pattern_match(surname) else 0.0
            origin_match = 1.0 if is_german_jewish_origin(surname) else 0.0
            
            # Calculate overall metric match score (average of count, rank, proportion)
            metric_match_score = (
                metric_scores['count_match'] * 0.35 +
                metric_scores['rank_match'] * 0.35 +
                metric_scores['proportion_match'] * 0.30
            )
            
            # Calculate linguistic score
            linguistic_score = (
                spelling_sim * 0.4 +
                phonetic_sim * 0.3 +
                pattern_match_score * 0.2 +
                origin_match * 0.1
            )
            
            # Combined score: 50% metrics, 40% linguistic, 10% origin bonus
            # Give bonus for origin match since it's one of the 4 required metrics
            origin_bonus = 0.1 if origin_match else 0.0
            overall_score = metric_match_score * 0.5 + linguistic_score * 0.4 + origin_bonus
            
            # Also calculate a "perfect match" score for surnames matching ALL metrics
            # This prioritizes surnames that match count, rank, proportion, AND origin
            perfect_match_score = (
                metric_match_score * 0.4 +
                linguistic_score * 0.3 +
                (1.0 if origin_match else 0.0) * 0.3  # 30% weight for origin
            )
            
            matches.append({
                'surname': surname,
                'us_count': data['count'],
                'us_rank': data['rank'],
                'us_proportion': data['proportion'],
                'us_prop100k': data['prop100k'],
                'count_match': metric_scores['count_match'],
                'rank_match': metric_scores['rank_match'],
                'proportion_match': metric_scores['proportion_match'],
                'metric_match_score': metric_match_score,
                'spelling_similarity': spelling_sim,
                'phonetic_similarity': phonetic_sim,
                'pattern_match': bool(pattern_match_score),
                'origin_match': bool(origin_match),
                'linguistic_score': linguistic_score,
                'overall_score': overall_score,
                'perfect_match_score': perfect_match_score,
                'length': len(surname),
            })
    
    # Sort by perfect_match_score first (for all-metric matches), then overall_score
    matches.sort(key=lambda x: (x['perfect_match_score'], x['overall_score']), reverse=True)
    
    return matches

def main():
    print("=" * 80)
    print("Finding surnames matching Adler across 4 metrics using U.S. Census 2010 data")
    print("=" * 80)
    print(f"\nAdler Baseline Metrics:")
    print(f"  U.S. Count: {ADLER_METRICS['us_count']:,}")
    print(f"  U.S. Rank: {ADLER_METRICS['us_rank']:,}")
    print(f"  U.S. Proportion: {ADLER_METRICS['us_proportion']*100:.4f}%")
    print(f"  U.S. Prop100k: {ADLER_METRICS['us_prop100k']}")
    print(f"  U.K. Proportion: {ADLER_METRICS['uk_proportion']*100:.4f}% (unverified)")
    print(f"  Origin: {ADLER_METRICS['origin']}")
    print()
    
    # Load census data
    print("Loading U.S. Census 2010 data...")
    census_data = load_census_data('Names_2010Census.csv')
    print(f"Loaded {len(census_data):,} surnames from census data")
    
    # Verify Adler data
    if 'ADLER' in census_data:
        adler_census = census_data['ADLER']
        print(f"\nVerified Adler in census:")
        print(f"  Count: {adler_census['count']:,} (expected: {ADLER_METRICS['us_count']:,})")
        print(f"  Rank: {adler_census['rank']:,} (expected: {ADLER_METRICS['us_rank']:,})")
        print(f"  Prop100k: {adler_census['prop100k']} (proportion: {adler_census['proportion']:.6f})")
        print()
    
    # Find metric matches
    print("Finding surnames matching Adler's metrics...")
    matches = find_metric_matches(census_data, ADLER_METRICS)
    
    print(f"\nFound {len(matches)} surnames matching Adler's demographic metrics")
    print()
    
    # Get top 50 matches
    top_50 = matches[:50]
    
    print("=" * 80)
    print(f"Top 50 Surnames Matching Adler Across All Metrics:")
    print("=" * 80)
    print(f"{'Rank':<6} {'Surname':<20} {'Count':<12} {'Rank':<8} {'Prop%':<10} {'Origin':<8} {'Metric':<8} {'Ling':<8} {'Perfect':<8}")
    print("-" * 80)
    
    for i, match in enumerate(top_50, 1):
        print(f"{i:<6} {match['surname']:<20} {match['us_count']:<12,} "
              f"{match['us_rank']:<8,} {match['us_proportion']*100:<10.4f} "
              f"{'Yes' if match['origin_match'] else 'No':<8} "
              f"{match['metric_match_score']:<8.3f} {match['linguistic_score']:<8.3f} "
              f"{match['perfect_match_score']:<8.3f}")
    
    # Find best overall match
    if matches:
        best_match = matches[0]
        
        print("\n" + "=" * 80)
        print(f"BEST MATCH: {best_match['surname']}")
        print("=" * 80)
        print(f"\nDemographic Metrics:")
        print(f"  U.S. Count: {best_match['us_count']:,} (Adler: {ADLER_METRICS['us_count']:,}, diff: {abs(best_match['us_count'] - ADLER_METRICS['us_count']):,})")
        print(f"  U.S. Rank: {best_match['us_rank']:,} (Adler: {ADLER_METRICS['us_rank']:,}, diff: {abs(best_match['us_rank'] - ADLER_METRICS['us_rank']):,})")
        print(f"  U.S. Proportion: {best_match['us_proportion']*100:.4f}% (Adler: {ADLER_METRICS['us_proportion']*100:.4f}%)")
        print(f"  Count Match Score: {best_match['count_match']:.3f}")
        print(f"  Rank Match Score: {best_match['rank_match']:.3f}")
        print(f"  Proportion Match Score: {best_match['proportion_match']:.3f}")
        print(f"  Overall Metric Match Score: {best_match['metric_match_score']:.3f}")
        
        print(f"\nLinguistic Similarity:")
        print(f"  Spelling Similarity: {best_match['spelling_similarity']:.3f}")
        print(f"  Phonetic Similarity: {best_match['phonetic_similarity']:.3f}")
        print(f"  Pattern Match: {'Yes' if best_match['pattern_match'] else 'No'}")
        print(f"  Origin Match: {'Yes' if best_match['origin_match'] else 'No'}")
        print(f"  Overall Linguistic Score: {best_match['linguistic_score']:.3f}")
        
        print(f"\nCombined Score: {best_match['overall_score']:.3f}")
    
    # Save results to JSON
    output = {
        'adler_metrics': ADLER_METRICS,
        'tolerance_ranges': {
            'count': f"{ADLER_METRICS['us_count'] * (1 - TOLERANCE['count']):,.0f} to {ADLER_METRICS['us_count'] * (1 + TOLERANCE['count']):,.0f}",
            'rank': f"{int(ADLER_METRICS['us_rank'] * (1 - TOLERANCE['rank'])):,} to {int(ADLER_METRICS['us_rank'] * (1 + TOLERANCE['rank'])):,}",
            'proportion': f"{ADLER_METRICS['us_proportion'] * (1 - TOLERANCE['proportion']):.6f} to {ADLER_METRICS['us_proportion'] * (1 + TOLERANCE['proportion']):.6f}",
        },
        'top_50_matches': top_50,
        'best_match': best_match if matches else None,
        'total_matches': len(matches)
    }
    
    with open('adler_metric_matches.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to adler_metric_matches.json")
    print(f"Total matches found: {len(matches)}")

if __name__ == '__main__':
    main()
