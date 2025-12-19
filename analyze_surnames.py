#!/usr/bin/env python3
"""
Analyze 2010 US Census surname data to find surnames matching Adler's statistics.
"""

import csv
import sys

# Adler baseline
ADLER_COUNT = 16412
ADLER_RANK = 2223
US_POPULATION_2010 = 308745538
ADLER_US_PCT = (ADLER_COUNT / US_POPULATION_2010) * 100

# Target ranges (±20% tolerance)
COUNT_MIN = int(ADLER_COUNT * 0.8)
COUNT_MAX = int(ADLER_COUNT * 1.2)
RANK_MIN = int(ADLER_RANK * 0.8)
RANK_MAX = int(ADLER_RANK * 1.2)
PCT_MIN = ADLER_US_PCT * 0.8
PCT_MAX = ADLER_US_PCT * 1.2

print("="*80)
print("FINDING SURNAMES MATCHING ADLER'S STATISTICS")
print("="*80)
print(f"\nAdler Baseline:")
print(f"  Count: {ADLER_COUNT:,}")
print(f"  Rank: {ADLER_RANK:,}")
print(f"  US Percentage: {ADLER_US_PCT:.4f}%")
print(f"\nTarget Ranges (±20%):")
print(f"  Count: {COUNT_MIN:,} - {COUNT_MAX:,}")
print(f"  Rank: {RANK_MIN:,} - {RANK_MAX:,}")
print(f"  Percentage: {PCT_MIN:.4f}% - {PCT_MAX:.4f}%")

# Read census data
matches = []
try:
    with open('Names_2010Census.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = row['name'].strip()
                count = int(row['count'].replace(',', ''))
                rank = int(row['rank'].replace(',', ''))
                
                # Calculate percentage
                pct = (count / US_POPULATION_2010) * 100
                
                # Check if matches all criteria
                if (COUNT_MIN <= count <= COUNT_MAX and 
                    RANK_MIN <= rank <= RANK_MAX and
                    PCT_MIN <= pct <= PCT_MAX):
                    matches.append({
                        'name': name,
                        'count': count,
                        'rank': rank,
                        'pct': pct
                    })
            except (ValueError, KeyError) as e:
                continue
except Exception as e:
    print(f"\nError reading file: {e}")
    sys.exit(1)

# Sort by rank
matches.sort(key=lambda x: x['rank'])

print(f"\n{'='*80}")
print(f"FOUND {len(matches)} MATCHING SURNAMES")
print(f"{'='*80}\n")

if matches:
    print(f"{'Rank':<8} {'Surname':<20} {'Count':<12} {'US %':<10}")
    print("-" * 80)
    for m in matches[:20]:  # Show first 20
        print(f"{m['rank']:<8} {m['name']:<20} {m['count']:<12,} {m['pct']:<10.4f}%")
    
    if len(matches) > 20:
        print(f"\n... and {len(matches) - 20} more matches")
    
    # Save top 12 matches
    print(f"\n{'='*80}")
    print("TOP 12 CLOSEST MATCHES (by rank proximity to Adler)")
    print(f"{'='*80}\n")
    
    # Sort by distance from Adler's rank
    matches_by_rank_distance = sorted(matches, key=lambda x: abs(x['rank'] - ADLER_RANK))
    top12 = matches_by_rank_distance[:12]
    
    print(f"{'Rank':<8} {'Surname':<20} {'Count':<12} {'US %':<10} {'Rank Diff':<10}")
    print("-" * 80)
    for m in top12:
        rank_diff = abs(m['rank'] - ADLER_RANK)
        print(f"{m['rank']:<8} {m['name']:<20} {m['count']:<12,} {m['pct']:<10.4f}% {rank_diff:<10}")
    
    # Save to file
    with open('matching_surnames.txt', 'w') as f:
        f.write("Surnames Matching Adler's Statistics\n")
        f.write("="*80 + "\n\n")
        f.write(f"Adler: Rank {ADLER_RANK}, Count {ADLER_COUNT:,}, US% {ADLER_US_PCT:.4f}%\n\n")
        f.write("Top 12 Matches:\n")
        f.write("-"*80 + "\n")
        for m in top12:
            f.write(f"{m['name']:<20} Rank: {m['rank']:<6} Count: {m['count']:<10,} US%: {m['pct']:.4f}%\n")
    
    print(f"\nResults saved to matching_surnames.txt")
else:
    print("\nNo matches found within ±20% tolerance.")
    print("Trying with ±25% tolerance...")
    
    # Try wider tolerance
    COUNT_MIN = int(ADLER_COUNT * 0.75)
    COUNT_MAX = int(ADLER_COUNT * 1.25)
    RANK_MIN = int(ADLER_RANK * 0.75)
    RANK_MAX = int(ADLER_RANK * 1.25)
    PCT_MIN = ADLER_US_PCT * 0.75
    PCT_MAX = ADLER_US_PCT * 1.25
    
    matches_wide = []
    with open('Names_2010Census.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = row['name'].strip()
                count = int(row['count'].replace(',', ''))
                rank = int(row['rank'].replace(',', ''))
                pct = (count / US_POPULATION_2010) * 100
                
                if (COUNT_MIN <= count <= COUNT_MAX and 
                    RANK_MIN <= rank <= RANK_MAX and
                    PCT_MIN <= pct <= PCT_MAX):
                    matches_wide.append({
                        'name': name,
                        'count': count,
                        'rank': rank,
                        'pct': pct
                    })
            except (ValueError, KeyError):
                continue
    
    matches_wide.sort(key=lambda x: abs(x['rank'] - ADLER_RANK))
    top12_wide = matches_wide[:12]
    
    if top12_wide:
        print(f"\nFound {len(matches_wide)} matches with ±25% tolerance")
        print(f"\n{'Rank':<8} {'Surname':<20} {'Count':<12} {'US %':<10}")
        print("-" * 80)
        for m in top12_wide:
            print(f"{m['rank']:<8} {m['name']:<20} {m['count']:<12,} {m['pct']:<10.4f}%")
