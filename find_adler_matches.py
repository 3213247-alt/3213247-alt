#!/usr/bin/env python3
"""
Find surnames matching Adler's statistics across multiple metrics:
- U.S. Census 2010: count=16,412, rank=2,223, proportion=0.0053%
- UK proportion: 0.004% (target)
"""

import csv
import urllib.request
import json
import math
from typing import List, Dict, Tuple

# Adler's known metrics
ADLER_US_COUNT = 16412
ADLER_US_RANK = 2223
ADLER_US_PROPORTION = 0.000053  # 0.0053%
ADLER_UK_PROPORTION = 0.00004   # 0.004% (target)
US_POPULATION_2010 = 308745538

# Tolerance ranges for matching
COUNT_TOLERANCE = 0.15  # ±15%
RANK_TOLERANCE = 0.15   # ±15%
PROP_TOLERANCE = 0.20   # ±20%


def download_us_census_data():
    """Download U.S. Census 2010 surname data"""
    url = "https://www2.census.gov/topics/genealogy/2010surnames/names.zip"
    print("Attempting to download U.S. Census surname data...")
    try:
        urllib.request.urlretrieve(url, "/workspace/us_surnames.zip")
        print("Downloaded US surnames data")
        return True
    except Exception as e:
        print(f"Could not download from Census.gov: {e}")
        return False


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
                    proportion = prop100k / 100000  # Convert per 100k to proportion
                    surnames.append({
                        'name': name,
                        'count': count,
                        'rank': rank,
                        'proportion': proportion,
                        'prop100k': prop100k
                    })
                except (ValueError, KeyError) as e:
                    continue
    except FileNotFoundError:
        print(f"File {filename} not found")
    return surnames


def calculate_similarity_score(surname: Dict, adler_metrics: Dict) -> float:
    """Calculate similarity score (0-1, higher is better match)"""
    scores = []
    
    # Count similarity
    count_diff = abs(surname['count'] - adler_metrics['count']) / adler_metrics['count']
    count_score = max(0, 1 - count_diff / COUNT_TOLERANCE)
    scores.append(count_score)
    
    # Rank similarity
    rank_diff = abs(surname['rank'] - adler_metrics['rank']) / adler_metrics['rank']
    rank_score = max(0, 1 - rank_diff / RANK_TOLERANCE)
    scores.append(rank_score)
    
    # Proportion similarity
    prop_diff = abs(surname['proportion'] - adler_metrics['proportion']) / adler_metrics['proportion']
    prop_score = max(0, 1 - prop_diff / PROP_TOLERANCE)
    scores.append(prop_score)
    
    # Average score
    return sum(scores) / len(scores)


def find_matching_surnames(us_surnames: List[Dict], adler_metrics: Dict) -> List[Tuple]:
    """Find surnames matching Adler's metrics"""
    matches = []
    
    for surname in us_surnames:
        # Check if within tolerance ranges
        count_match = abs(surname['count'] - adler_metrics['count']) / adler_metrics['count'] <= COUNT_TOLERANCE
        rank_match = abs(surname['rank'] - adler_metrics['rank']) / adler_metrics['rank'] <= RANK_TOLERANCE
        prop_match = abs(surname['proportion'] - adler_metrics['proportion']) / adler_metrics['proportion'] <= PROP_TOLERANCE
        
        if count_match and rank_match and prop_match:
            score = calculate_similarity_score(surname, adler_metrics)
            matches.append((surname, score))
    
    # Sort by similarity score (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches


def main():
    print("=" * 60)
    print("Finding surnames matching Adler's statistics")
    print("=" * 60)
    print(f"\nAdler Metrics:")
    print(f"  U.S. Count: {ADLER_US_COUNT:,}")
    print(f"  U.S. Rank: {ADLER_US_RANK:,}")
    print(f"  U.S. Proportion: {ADLER_US_PROPORTION*100:.4f}%")
    print(f"  UK Proportion (target): {ADLER_UK_PROPORTION*100:.4f}%")
    print(f"\nTolerance: ±{COUNT_TOLERANCE*100:.0f}% for count/rank, ±{PROP_TOLERANCE*100:.0f}% for proportion")
    
    # Try to get US Census data
    # First, try a direct CSV if available
    us_surnames = []
    
    # Try common filename patterns
    csv_files = [
        "/workspace/Names_2010Census.csv",
        "/workspace/app_c.csv",
        "/workspace/surnames.csv"
    ]
    
    for csv_file in csv_files:
        try:
            us_surnames = parse_us_census_csv(csv_file)
            if us_surnames:
                print(f"\nLoaded {len(us_surnames):,} surnames from {csv_file}")
                break
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            continue
    
    if not us_surnames:
        print("\nNo local CSV file found.")
        return
    
    if us_surnames:
        adler_metrics = {
            'count': ADLER_US_COUNT,
            'rank': ADLER_US_RANK,
            'proportion': ADLER_US_PROPORTION
        }
        
        matches = find_matching_surnames(us_surnames, adler_metrics)
        
        print(f"\nFound {len(matches)} matching surnames")
        print("\nTop 12 matches:")
        print("-" * 80)
        print(f"{'Rank':<6} {'Name':<20} {'Count':<12} {'US Rank':<10} {'Proportion':<12} {'Score':<8}")
        print("-" * 80)
        
        for i, (surname, score) in enumerate(matches[:12], 1):
            print(f"{i:<6} {surname['name']:<20} {surname['count']:<12,} {surname['rank']:<10,} {surname['proportion']*100:<11.4f}% {score:<8.3f}")
    else:
        print("\nNeed actual Census data file to proceed.")
        print("Please provide the US Census 2010 surname CSV file.")


if __name__ == "__main__":
    main()
