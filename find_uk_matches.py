#!/usr/bin/env python3
"""
Find surnames that match Adler's statistics in BOTH US and UK.
"""

# Top 12 US matches from previous analysis
us_matches = [
    {'name': 'ADLER', 'rank': 2223, 'count': 16412, 'us_pct': 0.0053},
    {'name': 'CHADWICK', 'rank': 2222, 'count': 16415, 'us_pct': 0.0053},
    {'name': 'BARNEY', 'rank': 2224, 'count': 16404, 'us_pct': 0.0053},
    {'name': 'WHITING', 'rank': 2221, 'count': 16418, 'us_pct': 0.0053},
    {'name': 'ONTIVEROS', 'rank': 2225, 'count': 16382, 'us_pct': 0.0053},
    {'name': 'ENNIS', 'rank': 2220, 'count': 16419, 'us_pct': 0.0053},
    {'name': 'RING', 'rank': 2226, 'count': 16381, 'us_pct': 0.0053},
    {'name': 'FOOTE', 'rank': 2219, 'count': 16425, 'us_pct': 0.0053},
    {'name': 'RIDER', 'rank': 2227, 'count': 16352, 'us_pct': 0.0053},
    {'name': 'HUSTON', 'rank': 2218, 'count': 16435, 'us_pct': 0.0053},
    {'name': 'JOINER', 'rank': 2228, 'count': 16349, 'us_pct': 0.0053},
    {'name': 'ALTMAN', 'rank': 2217, 'count': 16448, 'us_pct': 0.0053},
]

# UK target: ~0.004% (unverified, from secondary sources)
# UK population ~63 million (2010 estimate)
UK_POPULATION_2010 = 63000000  # approximate
ADLER_UK_PCT = 0.004
UK_COUNT_TARGET = (ADLER_UK_PCT / 100) * UK_POPULATION_2010  # ~2,520
UK_PCT_MIN = 0.0032  # ±20% of 0.004%
UK_PCT_MAX = 0.0048

print("="*80)
print("FINDING SURNAMES MATCHING ADLER IN BOTH US AND UK")
print("="*80)
print(f"\nUS Criteria (verified):")
print(f"  Count: ~13,130 - 19,694")
print(f"  Rank: ~1,778 - 2,668")
print(f"  US Percentage: ~0.0043% - 0.0064%")
print(f"\nUK Criteria (target):")
print(f"  UK Percentage: ~0.0032% - 0.0048%")
print(f"  UK Count (estimated): ~1,890 - 3,024")

print("\n" + "="*80)
print("TOP 12 US MATCHES - NEED UK VERIFICATION")
print("="*80)
print(f"\n{'Surname':<15} {'US Rank':<10} {'US Count':<12} {'US %':<10} {'Needs UK Data':<15}")
print("-" * 80)

for surname in us_matches:
    print(f"{surname['name']:<15} {surname['rank']:<10} {surname['count']:<12,} {surname['us_pct']:<10.4f}% {'Yes':<15}")

print("\n" + "="*80)
print("ANALYSIS")
print("="*80)
print("\nTo find the TRUE match, we need UK surname data for these 12 surnames.")
print("\nBased on surname origins and distribution patterns:")
print("- English surnames (CHADWICK, BARNEY, WHITING, ENNIS, FOOTE, RIDER, HUSTON, JOINER)")
print("  are more likely to have UK presence")
print("- German surnames (ADLER, ALTMAN) may have UK presence but likely lower")
print("- Spanish surnames (ONTIVEROS) unlikely to match UK percentage")

print("\n" + "="*80)
print("RECOMMENDED SURNAMES FOR UK VERIFICATION")
print("="*80)
print("\nMost likely to match UK percentage (English origin):")
print("1. CHADWICK - English surname")
print("2. BARNEY - English surname")
print("3. WHITING - English surname")
print("4. ENNIS - Irish/English surname")
print("5. FOOTE - English surname")
print("6. RIDER - English occupational surname")
print("7. HUSTON - Scottish/English surname")
print("8. JOINER - English occupational surname")
print("9. RING - English/German surname")
print("\nLess likely but possible:")
print("10. ADLER - German/Jewish surname")
print("11. ALTMAN - German/Jewish surname")
print("\nUnlikely:")
print("12. ONTIVEROS - Spanish surname (low UK presence)")
