#!/usr/bin/env python3
"""
Find surnames matching Adler's metrics across 4 dimensions:
1. U.S. count (16,412)
2. U.S. rank (2,223)
3. U.S. proportion (0.0053%)
4. U.K. proportion (0.004%)
"""

import csv
import math
from typing import List, Dict, Tuple

# Adler's target metrics
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 0.0053% as decimal
    'uk_proportion': 0.00004,   # 0.004% as decimal (unverified)
}

US_POPULATION_2010 = 308745538


def calculate_similarity_score(surname_data: Dict, target: Dict) -> float:
    """
    Calculate a composite similarity score across all 4 metrics.
    Lower score = better match (closer to 0).
    Uses normalized distance for each metric.
    """
    scores = []
    
    # 1. U.S. Count similarity (normalized by target)
    if surname_data.get('us_count'):
        count_diff = abs(surname_data['us_count'] - target['us_count'])
        count_score = count_diff / target['us_count']  # Normalized
        scores.append(count_score)
    
    # 2. U.S. Rank similarity (normalized by target)
    if surname_data.get('us_rank'):
        rank_diff = abs(surname_data['us_rank'] - target['us_rank'])
        rank_score = rank_diff / target['us_rank']  # Normalized
        scores.append(rank_score)
    
    # 3. U.S. Proportion similarity (absolute difference, then normalized)
    if surname_data.get('us_proportion'):
        prop_diff = abs(surname_data['us_proportion'] - target['us_proportion'])
        prop_score = prop_diff / target['us_proportion']  # Normalized
        scores.append(prop_score)
    elif surname_data.get('us_count'):
        # Calculate proportion from count
        calculated_prop = surname_data['us_count'] / US_POPULATION_2010
        prop_diff = abs(calculated_prop - target['us_proportion'])
        prop_score = prop_diff / target['us_proportion']
        scores.append(prop_score)
    
    # 4. U.K. Proportion similarity
    if surname_data.get('uk_proportion'):
        uk_diff = abs(surname_data['uk_proportion'] - target['uk_proportion'])
        uk_score = uk_diff / target['uk_proportion']  # Normalized
        scores.append(uk_score)
    
    # Return average of all available scores
    if scores:
        return sum(scores) / len(scores)
    return float('inf')


def find_matching_surnames(data_file: str, top_n: int = 50) -> List[Tuple[str, Dict, float]]:
    """
    Find surnames matching Adler's metrics.
    Returns list of (surname, data, similarity_score) tuples.
    """
    matches = []
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                surname = row.get('surname', '').strip()
                if not surname or surname.upper() == 'ADLER':
                    continue
                
                # Parse data
                surname_data = {}
                
                # U.S. count
                if 'us_count' in row and row['us_count']:
                    try:
                        surname_data['us_count'] = int(row['us_count'].replace(',', ''))
                    except:
                        pass
                
                # U.S. rank
                if 'us_rank' in row and row['us_rank']:
                    try:
                        surname_data['us_rank'] = int(row['us_rank'].replace(',', ''))
                    except:
                        pass
                
                # U.S. proportion
                if 'us_proportion' in row and row['us_proportion']:
                    try:
                        prop_str = row['us_proportion'].replace('%', '').strip()
                        surname_data['us_proportion'] = float(prop_str) / 100
                    except:
                        pass
                
                # U.K. proportion
                if 'uk_proportion' in row and row['uk_proportion']:
                    try:
                        prop_str = row['uk_proportion'].replace('%', '').strip()
                        surname_data['uk_proportion'] = float(prop_str) / 100
                    except:
                        pass
                
                # Calculate similarity
                score = calculate_similarity_score(surname_data, ADLER_METRICS)
                
                if score != float('inf'):
                    matches.append((surname, surname_data, score))
    
    except FileNotFoundError:
        print(f"Data file {data_file} not found.")
        return []
    except Exception as e:
        print(f"Error reading data file: {e}")
        return []
    
    # Sort by similarity score (lower is better)
    matches.sort(key=lambda x: x[2])
    
    return matches[:top_n]


def generate_sample_matches():
    """
    Generate a list of surnames that are likely close to Adler's metrics
    based on common surname patterns and known statistics.
    This is a fallback if no data file is available.
    """
    # These are example surnames that might be close - actual data needed
    sample_surnames = [
        # Surnames with similar rank range (2000-2500)
        # Surnames with similar count range (15000-18000)
        # Surnames with similar proportions
    ]
    return sample_surnames


if __name__ == '__main__':
    import sys
    
    # Try to find data file
    data_files = [
        'surnames.csv',
        'us_surnames.csv',
        'surname_data.csv',
        'census_surnames.csv',
    ]
    
    data_file = None
    for df in data_files:
        try:
            with open(df, 'r'):
                data_file = df
                break
        except:
            continue
    
    if not data_file:
        print("No surname data file found.")
        print("Expected format: CSV with columns: surname, us_count, us_rank, us_proportion, uk_proportion")
        print("\nAdler target metrics:")
        print(f"  U.S. Count: {ADLER_METRICS['us_count']:,}")
        print(f"  U.S. Rank: {ADLER_METRICS['us_rank']:,}")
        print(f"  U.S. Proportion: {ADLER_METRICS['us_proportion']*100:.4f}%")
        print(f"  U.K. Proportion: {ADLER_METRICS['uk_proportion']*100:.4f}%")
        sys.exit(1)
    
    print(f"Analyzing surnames from {data_file}...")
    matches = find_matching_surnames(data_file, top_n=50)
    
    if matches:
        print(f"\nTop 50 surnames matching Adler's metrics:\n")
        print(f"{'Rank':<6} {'Surname':<20} {'US Count':<12} {'US Rank':<10} {'US %':<10} {'UK %':<10} {'Score':<10}")
        print("-" * 90)
        
        for i, (surname, data, score) in enumerate(matches, 1):
            us_count = data.get('us_count', 'N/A')
            us_rank = data.get('us_rank', 'N/A')
            us_prop = data.get('us_proportion', 'N/A')
            if us_prop != 'N/A':
                us_prop = f"{us_prop*100:.4f}%"
            uk_prop = data.get('uk_proportion', 'N/A')
            if uk_prop != 'N/A':
                uk_prop = f"{uk_prop*100:.4f}%"
            
            print(f"{i:<6} {surname:<20} {str(us_count):<12} {str(us_rank):<10} {str(us_prop):<10} {str(uk_prop):<10} {score:.6f}")
        
        # Best match
        best_surname, best_data, best_score = matches[0]
        print(f"\n{'='*90}")
        print(f"BEST MATCH: {best_surname}")
        print(f"Similarity Score: {best_score:.6f} (lower is better)")
        print(f"\nMetrics:")
        print(f"  U.S. Count: {best_data.get('us_count', 'N/A')} (target: {ADLER_METRICS['us_count']:,})")
        print(f"  U.S. Rank: {best_data.get('us_rank', 'N/A')} (target: {ADLER_METRICS['us_rank']:,})")
        print(f"  U.S. Proportion: {best_data.get('us_proportion', 'N/A')} (target: {ADLER_METRICS['us_proportion']:.6f})")
        print(f"  U.K. Proportion: {best_data.get('uk_proportion', 'N/A')} (target: {ADLER_METRICS['uk_proportion']:.6f})")
    else:
        print("No matching surnames found.")
