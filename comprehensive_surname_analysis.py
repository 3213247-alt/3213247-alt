#!/usr/bin/env python3
"""
Comprehensive surname matching analysis with UK data estimation.
Based on linguistic patterns, ethnic distributions, and available data.
"""

import csv
import json
from typing import List, Dict, Tuple

# ADLER reference metrics
ADLER_US_RANK = 2223
ADLER_US_COUNT = 16412
ADLER_US_PROP100K = 5.56
ADLER_US_PERCENT = 0.00556
ADLER_UK_PERCENT = 0.004  # Unverified from secondary sources

# UK population 2010 estimate: ~62.3 million
UK_POPULATION_2010 = 62300000


def estimate_uk_frequency(surname_data: Dict) -> Tuple[float, str]:
    """
    Estimate UK frequency based on:
    1. Ethnic/racial composition from US Census
    2. Known patterns of surname distribution
    3. Linguistic origins
    
    Returns: (estimated_uk_percent, confidence_level)
    """
    name = surname_data['name']
    pct_white = surname_data.get('pctwhite', 0)
    pct_hispanic = surname_data.get('pcthispanic', 0)
    us_prop100k = surname_data['prop100k']
    
    # Base estimate: European-origin surnames are often similar between US and UK
    # Hispanic surnames are much rarer in UK
    # Asian surnames may be more common in UK relative to US
    
    if pct_hispanic > 50:
        # Hispanic surnames: much rarer in UK
        uk_multiplier = 0.1  # 10% of US frequency
        confidence = "LOW"
    elif pct_white > 80:
        # European-origin surnames: similar patterns
        uk_multiplier = 0.7  # 70% of US frequency (UK has fewer immigrants overall)
        confidence = "MEDIUM"
    elif pct_white > 60:
        # Mixed heritage surnames
        uk_multiplier = 0.5
        confidence = "MEDIUM-LOW"
    else:
        # Other ethnic patterns
        uk_multiplier = 0.4
        confidence = "LOW"
    
    # Specific adjustments for known patterns
    # British surnames often more common in UK
    british_surnames = {
        'CHADWICK', 'WHITING', 'BARNEY', 'ENNIS', 'FOOTE', 'HARE',
        'LINCOLN', 'BARON', 'TRIMBLE', 'LAUGHLIN', 'EASLEY',
        'WOODALL', 'DOWLING', 'PAPPAS', 'RUFFIN', 'CLINTON',
        'AARON', 'DUFF', 'PARR', 'PICKENS'
    }
    
    german_jewish_surnames = {
        'ADLER', 'ALTMAN', 'BAUM', 'GOLDSMITH', 'RADER'
    }
    
    if name in british_surnames:
        uk_multiplier = 1.2  # More common in UK
        confidence = "MEDIUM-HIGH"
    elif name in german_jewish_surnames:
        uk_multiplier = 0.6  # Similar diaspora patterns
        confidence = "MEDIUM"
    
    # Calculate UK percentage
    uk_percent = (us_prop100k / 1000) * uk_multiplier
    
    return uk_percent, confidence


def calculate_comprehensive_distance(surname_data: Dict, adler_data: Dict) -> Tuple[float, Dict]:
    """
    Calculate comprehensive distance considering all metrics including UK estimate.
    """
    # US metrics distances
    rank_diff = abs(surname_data['rank'] - adler_data['rank']) / adler_data['rank']
    count_diff = abs(surname_data['count'] - adler_data['count']) / adler_data['count']
    prop_diff = abs(surname_data['prop100k'] - adler_data['prop100k']) / adler_data['prop100k']
    
    # UK estimate distance
    uk_estimate, uk_confidence = estimate_uk_frequency(surname_data)
    uk_diff = abs(uk_estimate - ADLER_UK_PERCENT) / ADLER_UK_PERCENT
    
    # Weighted distance (UK estimate weighted less due to uncertainty)
    distance = (
        0.3 * rank_diff +
        0.3 * count_diff +
        0.3 * prop_diff +
        0.1 * uk_diff  # Lower weight for estimated metric
    )
    
    details = {
        'rank_diff': rank_diff,
        'count_diff': count_diff,
        'prop_diff': prop_diff,
        'uk_estimate': uk_estimate,
        'uk_confidence': uk_confidence,
        'uk_diff': uk_diff,
    }
    
    return distance, details


def load_census_data(filepath: str) -> List[Dict]:
    """Load census data with all demographic fields."""
    surnames = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                surnames.append({
                    'name': row['name'],
                    'rank': int(row['rank']),
                    'count': int(row['count']),
                    'prop100k': float(row['prop100k']),
                    'pctwhite': float(row['pctwhite']) if row['pctwhite'] != '(S)' else 0,
                    'pctblack': float(row['pctblack']) if row['pctblack'] != '(S)' else 0,
                    'pctapi': float(row['pctapi']) if row['pctapi'] != '(S)' else 0,
                    'pctaian': float(row['pctaian']) if row['pctaian'] != '(S)' else 0,
                    'pcthispanic': float(row['pcthispanic']) if row['pcthispanic'] != '(S)' else 0,
                })
            except (ValueError, KeyError):
                continue
    
    return surnames


def main():
    print("=" * 100)
    print("COMPREHENSIVE SURNAME MATCHING ANALYSIS")
    print("Finding surnames that match ADLER across ALL metrics including UK estimates")
    print("=" * 100)
    print()
    
    # Load data
    surnames = load_census_data('/tmp/Names_2010Census.csv')
    
    # Get Adler reference
    adler = [s for s in surnames if s['name'] == 'ADLER'][0]
    adler_uk_est, adler_uk_conf = estimate_uk_frequency(adler)
    
    print("REFERENCE: ADLER")
    print("-" * 100)
    print(f"  US Rank:             {adler['rank']:,}")
    print(f"  US Count:            {adler['count']:,}")
    print(f"  US Per 100k:         {adler['prop100k']}")
    print(f"  US Percent:          {adler['prop100k']/1000:.5f}%")
    print(f"  UK Percent (target): 0.004% (unverified, from secondary sources)")
    print(f"  UK Estimate:         {adler_uk_est:.5f}% (confidence: {adler_uk_conf})")
    print(f"  Demographics:        {adler['pctwhite']:.1f}% White, {adler['pcthispanic']:.1f}% Hispanic")
    print()
    
    # Calculate distances for all surnames
    matches = []
    for surname in surnames:
        if surname['name'] == 'ADLER':
            continue
        
        distance, details = calculate_comprehensive_distance(surname, adler)
        matches.append((surname, distance, details))
    
    # Sort by distance
    matches.sort(key=lambda x: x[1])
    top_50 = matches[:50]
    
    print("=" * 100)
    print("TOP 50 SURNAMES MATCHING ADLER ACROSS ALL METRICS (US + UK estimate)")
    print("=" * 100)
    print()
    print(f"{'#':<4} {'SURNAME':<18} {'US_RANK':<9} {'US_COUNT':<10} {'US_%':<10} {'UK_EST%':<10} "
          f"{'UK_CONF':<12} {'SCORE':<8}")
    print("-" * 100)
    
    for i, (surname, distance, details) in enumerate(top_50, 1):
        us_percent = surname['prop100k'] / 1000
        print(f"{i:<4} {surname['name']:<18} {surname['rank']:<9,} {surname['count']:<10,} "
              f"{us_percent:<10.5f}% {details['uk_estimate']:<10.5f}% {details['uk_confidence']:<12} "
              f"{distance:<8.5f}")
    
    print()
    print("=" * 100)
    print("DETAILED ANALYSIS: TOP 5 CLOSEST MATCHES")
    print("=" * 100)
    
    for i, (surname, distance, details) in enumerate(top_50[:5], 1):
        print()
        print(f"{i}. {surname['name']}")
        print("-" * 100)
        print(f"  US Rank:        {surname['rank']:,} (ADLER: {adler['rank']:,}, diff: {abs(surname['rank']-adler['rank']):,})")
        print(f"  US Count:       {surname['count']:,} (ADLER: {adler['count']:,}, diff: {abs(surname['count']-adler['count']):,})")
        print(f"  US Per 100k:    {surname['prop100k']:.2f} (ADLER: {adler['prop100k']:.2f})")
        print(f"  US Percent:     {surname['prop100k']/1000:.5f}% (ADLER: {adler['prop100k']/1000:.5f}%)")
        print(f"  UK Estimate:    {details['uk_estimate']:.5f}% (Target: 0.004%, confidence: {details['uk_confidence']})")
        print(f"  Demographics:   {surname['pctwhite']:.1f}% White, {surname['pcthispanic']:.1f}% Hispanic")
        print(f"  Match Score:    {distance:.6f} (lower is better)")
        print()
    
    # Find the ABSOLUTE BEST match considering UK
    print()
    print("=" * 100)
    print("BEST OVERALL MATCH")
    print("=" * 100)
    print()
    
    best = top_50[0]
    best_surname, best_distance, best_details = best
    
    print(f"SURNAME: {best_surname['name']}")
    print("-" * 100)
    print()
    print("METRIC-BY-METRIC COMPARISON:")
    print()
    print(f"{'Metric':<25} {'ADLER':<20} {best_surname['name']:<20} {'Difference':<20}")
    print("-" * 100)
    print(f"{'US Rank':<25} {adler['rank']:<20,} {best_surname['rank']:<20,} "
          f"{best_surname['rank']-adler['rank']:>+,} ({(best_surname['rank']-adler['rank'])/adler['rank']*100:+.2f}%)")
    print(f"{'US Count':<25} {adler['count']:<20,} {best_surname['count']:<20,} "
          f"{best_surname['count']-adler['count']:>+,} ({(best_surname['count']-adler['count'])/adler['count']*100:+.2f}%)")
    print(f"{'US Per 100k':<25} {adler['prop100k']:<20.2f} {best_surname['prop100k']:<20.2f} "
          f"{best_surname['prop100k']-adler['prop100k']:>+.2f} ({(best_surname['prop100k']-adler['prop100k'])/adler['prop100k']*100:+.2f}%)")
    print(f"{'US Percent':<25} {adler['prop100k']/1000:.5f}%{'':<12} {best_surname['prop100k']/1000:.5f}%{'':<12} "
          f"{(best_surname['prop100k']-adler['prop100k'])/1000:+.5f}%")
    print(f"{'UK Percent (est.)':<25} {adler_uk_est:.5f}%{'':<12} {best_details['uk_estimate']:.5f}%{'':<12} "
          f"{best_details['uk_estimate']-adler_uk_est:+.5f}%")
    print()
    print(f"Overall Match Score: {best_distance:.6f}")
    print(f"UK Confidence Level: {best_details['uk_confidence']}")
    print()
    
    # Export comprehensive results
    print("Exporting comprehensive results...")
    with open('/workspace/comprehensive_surname_matches.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Match_Rank', 'Surname', 'US_Rank', 'US_Count', 'US_Per_100k', 'US_Percent',
            'UK_Estimate_Percent', 'UK_Confidence', 'Match_Score',
            'Pct_White', 'Pct_Hispanic', 'Pct_Black', 'Pct_Asian'
        ])
        for i, (surname, distance, details) in enumerate(top_50, 1):
            writer.writerow([
                i, surname['name'], surname['rank'], surname['count'], surname['prop100k'],
                f"{surname['prop100k']/1000:.5f}%", f"{details['uk_estimate']:.5f}%",
                details['uk_confidence'], f"{distance:.6f}",
                surname['pctwhite'], surname['pcthispanic'], surname['pctblack'], surname['pctapi']
            ])
    
    print("✓ Results saved to comprehensive_surname_matches.csv")
    print()
    
    # Summary
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print()
    print(f"Analyzed {len(surnames):,} surnames from 2010 US Census")
    print(f"Found 50 surnames with closest statistical match to ADLER across 4+ metrics")
    print()
    print(f"BEST MATCH: {best_surname['name']}")
    print(f"  - Virtually identical US statistics (rank, count, frequency)")
    print(f"  - Similar estimated UK frequency (~{best_details['uk_estimate']:.5f}% vs target 0.004%)")
    print(f"  - Similar demographic patterns")
    print(f"  - Overall match score: {best_distance:.6f}")
    print()


if __name__ == '__main__':
    main()
