#!/usr/bin/env python3
"""
Research surnames with statistics matching Adler across US and UK metrics.

Based on known surname distribution patterns and rank proximity analysis.
"""

# Adler baseline (2010 US Census)
ADLER = {
    'surname': 'Adler',
    'us_count': 16412,
    'us_rank': 2223,
    'us_pct': 0.0053,  # 16,412 / 308,745,538
    'uk_pct': 0.004    # unverified, from secondary sources
}

# Target ranges (±20% tolerance)
TARGET_RANGES = {
    'us_count': (13130, 19694),      # ±20% of 16,412
    'us_rank': (1778, 2668),         # ±20% of 2,223
    'us_pct': (0.0042, 0.0064),      # ±20% of 0.0053%
    'uk_pct': (0.0032, 0.0048)       # ±20% of 0.004%
}

print("="*70)
print("SURNAME MATCHING ANALYSIS: Finding surnames similar to Adler")
print("="*70)
print(f"\nAdler Baseline:")
print(f"  US Count: {ADLER['us_count']:,}")
print(f"  US Rank: {ADLER['us_rank']:,}")
print(f"  US Percentage: {ADLER['us_pct']}%")
print(f"  UK Percentage: {ADLER['uk_pct']}%")
print(f"\nTarget Ranges (±20% tolerance):")
print(f"  US Count: {TARGET_RANGES['us_count'][0]:,} - {TARGET_RANGES['us_count'][1]:,}")
print(f"  US Rank: {TARGET_RANGES['us_rank'][0]:,} - {TARGET_RANGES['us_rank'][1]:,}")
print(f"  US Percentage: {TARGET_RANGES['us_pct'][0]}% - {TARGET_RANGES['us_pct'][1]}%")
print(f"  UK Percentage: {TARGET_RANGES['uk_pct'][0]}% - {TARGET_RANGES['uk_pct'][1]}%")

print("\n" + "="*70)
print("CANDIDATE SURNAMES FOR VERIFICATION")
print("="*70)
print("\nBased on surname distribution patterns, surnames near rank 2,223")
print("in the 2010 US Census likely include:")
print("\nNote: These require verification against actual census data.")
print("\nSurnames to investigate (alphabetically near rank 2,223):")

# Common surnames that might be in this rank range
# These are educated estimates based on surname frequency patterns
candidates = [
    "Ackerman", "Aldrich", "Allison", "Alston", "Andersen", 
    "Armstrong", "Atkinson", "Avery", "Baldwin", "Barker",
    "Barnett", "Barrett"
]

for i, surname in enumerate(candidates, 1):
    print(f"{i:2d}. {surname}")

print("\n" + "="*70)
print("VERIFICATION REQUIRED")
print("="*70)
print("\nTo find the TRUE matches, we need:")
print("1. Access to 2010 US Census surname data file")
print("2. Surnames with rank between 1,778 - 2,668")
print("3. Count verification (13,130 - 19,694)")
print("4. UK surname data for cross-reference")
print("5. Percentage calculations for both countries")
