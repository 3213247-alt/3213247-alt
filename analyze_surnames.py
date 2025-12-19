
def calculate_metrics(count, population):
    return (count / population) * 100

us_pop_2010 = 308745538
uk_pop_2011 = 63182000

# Adler Data (Target)
adler_us_count = 16412
adler_us_rank = 2223
adler_us_pct = calculate_metrics(adler_us_count, us_pop_2010)
adler_uk_pct = 0.004  # User provided

print(f"Adler US Pct: {adler_us_pct:.6f}%")
print(f"Adler UK Pct: {adler_uk_pct:.6f}%")

# Candidates with estimated data (based on typical rank ~2200 stats)
# I need to find names with US Count ~16,400 and UK Count ~2,500
candidates = [
    {"name": "Stahl", "us_count": 16688, "us_rank": 2176, "uk_count_est": 2000}, # German
    {"name": "Fink", "us_count": 16400, "us_rank": 2230, "uk_count_est": 1800},  # German
    {"name": "Urban", "us_count": 16400, "us_rank": 2220, "uk_count_est": 2500}, # Mixed
    {"name": "Link", "us_count": 16500, "us_rank": 2210, "uk_count_est": 3500},  # English/German
    {"name": "Haggerty", "us_count": 16200, "us_rank": 2250, "uk_count_est": 3000}, # Irish
    {"name": "Lyle", "us_count": 15800, "us_rank": 2300, "uk_count_est": 4000},  # Scottish
    {"name": "Neff", "us_count": 15500, "us_rank": 2350, "uk_count_est": 1500},  # German
    {"name": "Brink", "us_count": 15800, "us_rank": 2300, "uk_count_est": 2000}, # Dutch/German
    {"name": "Metz", "us_count": 17000, "us_rank": 2100, "uk_count_est": 2000},  # German
    {"name": "Curran", "us_count": 16500, "us_rank": 2200, "uk_count_est": 6000}, # Irish (Common in UK)
    {"name": "Groves", "us_count": 17000, "us_rank": 2100, "uk_count_est": 12000}, # English (Common in UK)
    {"name": "Dolan", "us_count": 16000, "us_rank": 2280, "uk_count_est": 8000}, # Irish
]

print("\nAnalysis:")
print(f"{'Name':<12} {'US Rank':<8} {'US Count':<10} {'US %':<10} {'UK % (Est)':<10} {'Diff US Count':<10}")

closest = None
min_diff = float('inf')

for c in candidates:
    us_pct = calculate_metrics(c['us_count'], us_pop_2010)
    uk_pct = calculate_metrics(c['uk_count_est'], uk_pop_2011)
    
    # Calculate difference score (normalized)
    diff_us = abs(c['us_count'] - adler_us_count)
    diff_uk = abs(uk_pct - adler_uk_pct)
    
    # Heuristic score: sum of % errors
    # US error
    us_err = diff_us / adler_us_count
    # UK error
    uk_err = diff_uk / adler_uk_pct
    
    score = us_err + uk_err
    
    print(f"{c['name']:<12} {c['us_rank']:<8} {c['us_count']:<10} {us_pct:.6f}%  {uk_pct:.6f}%   {diff_us:<10}")
    
    if score < min_diff:
        min_diff = score
        closest = c

print(f"\nClosest Match: {closest['name']}")
