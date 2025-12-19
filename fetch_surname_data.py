#!/usr/bin/env python3
"""
Fetch and process surname data from various sources to find matches for Adler.
"""

import requests
import csv
import json
from typing import Dict, List, Optional

# Adler target metrics
ADLER_TARGET = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,
    'uk_proportion': 0.00004,
}

US_POP_2010 = 308745538


def fetch_forebears_data(surname: str) -> Optional[Dict]:
    """Fetch data from Forebears.io API (if available)"""
    try:
        # Note: Forebears may require API key or have rate limits
        url = f"https://forebears.io/surnames/{surname.lower()}"
        # This is a placeholder - actual API may differ
        return None
    except:
        return None


def create_surname_database_from_known_sources():
    """
    Create a database of surnames with similar metrics to Adler.
    Based on known surname statistics and patterns.
    """
    # Surnames in similar rank range (2000-2500) with similar characteristics
    # These are educated guesses - actual data needed for precision
    
    similar_surnames = []
    
    # We need actual data sources. Let me create a structure for manual entry
    # or data import
    
    return similar_surnames


def calculate_match_score(surname_data: Dict) -> float:
    """Calculate how close a surname matches Adler's metrics"""
    score = 0.0
    factors = 0
    
    # US Count match (within 20% = good match)
    if 'us_count' in surname_data:
        count_diff = abs(surname_data['us_count'] - ADLER_TARGET['us_count'])
        count_ratio = count_diff / ADLER_TARGET['us_count']
        score += count_ratio
        factors += 1
    
    # US Rank match (within 20% = good match)
    if 'us_rank' in surname_data:
        rank_diff = abs(surname_data['us_rank'] - ADLER_TARGET['us_rank'])
        rank_ratio = rank_diff / ADLER_TARGET['us_rank']
        score += rank_ratio
        factors += 1
    
    # US Proportion match
    if 'us_proportion' in surname_data:
        prop_diff = abs(surname_data['us_proportion'] - ADLER_TARGET['us_proportion'])
        prop_ratio = prop_diff / ADLER_TARGET['us_proportion']
        score += prop_ratio
        factors += 1
    elif 'us_count' in surname_data:
        calc_prop = surname_data['us_count'] / US_POP_2010
        prop_diff = abs(calc_prop - ADLER_TARGET['us_proportion'])
        prop_ratio = prop_diff / ADLER_TARGET['us_proportion']
        score += prop_ratio
        factors += 1
    
    # UK Proportion match
    if 'uk_proportion' in surname_data:
        uk_diff = abs(surname_data['uk_proportion'] - ADLER_TARGET['uk_proportion'])
        uk_ratio = uk_diff / ADLER_TARGET['uk_proportion']
        score += uk_ratio
        factors += 1
    
    if factors == 0:
        return float('inf')
    
    return score / factors


if __name__ == '__main__':
    print("Surname matching tool for Adler")
    print("=" * 50)
    print("\nTarget metrics:")
    print(f"  U.S. Count: {ADLER_TARGET['us_count']:,}")
    print(f"  U.S. Rank: {ADLER_TARGET['us_rank']:,}")
    print(f"  U.S. Proportion: {ADLER_TARGET['us_proportion']*100:.4f}%")
    print(f"  U.K. Proportion: {ADLER_TARGET['uk_proportion']*100:.4f}%")
    print("\nNote: Actual surname data file needed for matching.")
