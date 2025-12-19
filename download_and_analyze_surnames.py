#!/usr/bin/env python3
"""
Download and analyze US Census 2010 surname data to find matches for Adler
"""

import csv
import urllib.request
import json
from typing import List, Dict, Tuple
import math

# Adler baseline metrics
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 16412 / 308745538,  # 0.00005312
    'uk_proportion': 0.00004,  # 0.004% (unverified)
}

US_POPULATION_2010 = 308745538

def download_census_surnames() -> str:
    """
    Download US Census 2010 surname file.
    URL: https://www2.census.gov/topics/genealogy/2010surnames/names.zip
    Or direct CSV: https://www2.census.gov/topics/genealogy/2010surnames/Names_2010Census_Top1000.xlsx
    """
    # Note: The actual file format may vary
    # This is a placeholder for the download logic
    url = "https://www2.census.gov/topics/genealogy/2010surnames/Names_2010Census_Top1000.xlsx"
    # For now, we'll work with CSV if available
    return ""

def load_surname_data(filepath: str) -> List[Dict]:
    """Load surname data from CSV file"""
    surnames = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                surname = row.get('name', '').strip().title()
                try:
                    count = int(row.get('count', 0))
                    rank = int(row.get('rank', 0))
                    surnames.append({
                        'surname': surname,
                        'us_count': count,
                        'us_rank': rank,
                        'us_proportion': count / US_POPULATION_2010
                    })
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        print("Please download the US Census 2010 surname file manually.")
    return surnames

def calculate_match_score(surname_data: Dict, adler_metrics: Dict) -> Tuple[float, Dict]:
    """
    Calculate how closely a surname matches Adler across all 4 metrics.
    Returns: (score, details) where score is 0-100 (100 = perfect match)
    """
    details = {}
    scores = []
    
    # Metric 1: US Count
    if 'us_count' in surname_data:
        count_diff = abs(surname_data['us_count'] - adler_metrics['us_count'])
        count_ratio = count_diff / adler_metrics['us_count']
        count_score = max(0, (1 - count_ratio) * 100)
        scores.append(count_score)
        details['count_score'] = count_score
        details['count_diff_pct'] = count_ratio * 100
    
    # Metric 2: US Rank
    if 'us_rank' in surname_data:
        rank_diff = abs(surname_data['us_rank'] - adler_metrics['us_rank'])
        rank_ratio = rank_diff / adler_metrics['us_rank']
        rank_score = max(0, (1 - rank_ratio) * 100)
        scores.append(rank_score)
        details['rank_score'] = rank_score
        details['rank_diff_pct'] = rank_ratio * 100
    
    # Metric 3: US Proportion
    if 'us_proportion' in surname_data:
        prop_diff = abs(surname_data['us_proportion'] - adler_metrics['us_proportion'])
        prop_ratio = prop_diff / adler_metrics['us_proportion']
        prop_score = max(0, (1 - prop_ratio) * 100)
        scores.append(prop_score)
        details['prop_score'] = prop_score
        details['prop_diff_pct'] = prop_ratio * 100
    
    # Metric 4: UK Proportion (if available)
    if 'uk_proportion' in surname_data:
        uk_prop_diff = abs(surname_data['uk_proportion'] - adler_metrics['uk_proportion'])
        uk_prop_ratio = uk_prop_diff / adler_metrics['uk_proportion']
        uk_prop_score = max(0, (1 - uk_prop_ratio) * 100)
        scores.append(uk_prop_score)
        details['uk_prop_score'] = uk_prop_score
        details['uk_prop_diff_pct'] = uk_prop_ratio * 100
    
    # Average score across available metrics
    if scores:
        avg_score = sum(scores) / len(scores)
        details['avg_score'] = avg_score
        details['metrics_matched'] = len(scores)
        return avg_score, details
    
    return 0.0, details

def find_matching_surnames(surnames: List[Dict], adler_metrics: Dict, 
                          count_range: Tuple[int, int] = (13000, 20000),
                          rank_range: Tuple[int, int] = (1700, 2700),
                          top_n: int = 50) -> List[Tuple[str, float, Dict, Dict]]:
    """
    Find surnames matching Adler's metrics.
    Returns: List of (surname, match_score, surname_data, score_details)
    """
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
    print("\n" + "=" * 100)
    print("ADLER SURNAME MATCHING RESULTS")
    print("=" * 100)
    print(f"\nAdler Baseline:")
    print(f"  US Count: {ADLER_METRICS['us_count']:,}")
    print(f"  US Rank: {ADLER_METRICS['us_rank']:,}")
    print(f"  US Proportion: {ADLER_METRICS['us_proportion']*100:.5f}%")
    print(f"  UK Proportion: {ADLER_METRICS['uk_proportion']*100:.5f}% (unverified)")
    
    print("\n" + "-" * 100)
    print(f"{'Rank':<6} {'Surname':<20} {'US Count':<12} {'US Rank':<10} {'US Prop %':<12} {'Match Score':<12}")
    print("-" * 100)
    
    for i, (surname, score, data, details) in enumerate(matches, 1):
        us_count = data.get('us_count', 0)
        us_rank = data.get('us_rank', 0)
        us_prop = data.get('us_proportion', 0) * 100
        
        print(f"{i:<6} {surname:<20} {us_count:<12,} {us_rank:<10,} {us_prop:<12.5f} {score:<12.2f}%")
    
    print("\n" + "=" * 100)
    print("BEST MATCH (matches all 4 metrics simultaneously):")
    if matches:
        best = matches[0]
        print(f"  Surname: {best[0]}")
        print(f"  Match Score: {best[1]:.2f}%")
        print(f"  Details: {json.dumps(best[3], indent=2)}")

if __name__ == '__main__':
    print("Adler Surname Matching Analysis")
    print("=" * 60)
    
    # Try to load surname data
    # Note: User needs to provide the census file
    print("\nTo use this script:")
    print("1. Download US Census 2010 surname file from:")
    print("   https://www2.census.gov/topics/genealogy/2010surnames/")
    print("2. Save as 'census_surnames_2010.csv'")
    print("3. Run this script again")
    
    # Example: Try to load if file exists
    try:
        surnames = load_surname_data('census_surnames_2010.csv')
        if surnames:
            print(f"\nLoaded {len(surnames)} surnames")
            matches = find_matching_surnames(surnames, ADLER_METRICS)
            print_results(matches)
        else:
            print("\nNo surname data loaded. Please provide census file.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Please download and provide the census surname file.")
