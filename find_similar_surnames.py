#!/usr/bin/env python3
"""
Find surnames with statistics similar to Adler across US and UK metrics.

Adler baseline:
- US count: 16,412
- US rank: 2,223
- US percentage: 0.0053% (16,412 / 308,745,538)
- UK percentage: ~0.004% (unverified)
"""

# Target ranges for matching surnames (±20% tolerance)
ADLER_US_COUNT = 16412
ADLER_US_RANK = 2223
ADLER_US_PCT = 0.0053
ADLER_UK_PCT = 0.004

# Tolerance ranges
COUNT_TOLERANCE = 0.20  # ±20%
RANK_TOLERANCE = 0.20   # ±20%
PCT_TOLERANCE = 0.20    # ±20%

def calculate_match_score(us_count, us_rank, us_pct, uk_pct):
    """Calculate how closely a surname matches Adler's metrics."""
    scores = []
    
    # US count match (0-1 score)
    count_diff = abs(us_count - ADLER_US_COUNT) / ADLER_US_COUNT
    count_score = max(0, 1 - (count_diff / COUNT_TOLERANCE))
    scores.append(('count', count_score))
    
    # US rank match (0-1 score)
    rank_diff = abs(us_rank - ADLER_US_RANK) / ADLER_US_RANK
    rank_score = max(0, 1 - (rank_diff / RANK_TOLERANCE))
    scores.append(('rank', rank_score))
    
    # US percentage match (0-1 score)
    pct_diff = abs(us_pct - ADLER_US_PCT) / ADLER_US_PCT
    pct_score = max(0, 1 - (pct_diff / PCT_TOLERANCE))
    scores.append(('us_pct', pct_score))
    
    # UK percentage match (0-1 score)
    uk_pct_diff = abs(uk_pct - ADLER_UK_PCT) / ADLER_UK_PCT if ADLER_UK_PCT > 0 else 0
    uk_pct_score = max(0, 1 - (uk_pct_diff / PCT_TOLERANCE))
    scores.append(('uk_pct', uk_pct_score))
    
    # Overall match score (average of all metrics)
    overall_score = sum(s[1] for s in scores) / len(scores)
    
    return {
        'overall': overall_score,
        'scores': scores,
        'matches_all': all(s[1] > 0.8 for s in scores)  # 80% match threshold
    }

# Example surnames with similar statistics (these would come from actual census data)
# Format: (surname, us_count, us_rank, us_pct, uk_pct)
# Note: These are hypothetical examples - we need actual census data

print("Adler Baseline Statistics:")
print(f"  US Count: {ADLER_US_COUNT:,}")
print(f"  US Rank: {ADLER_US_RANK:,}")
print(f"  US Percentage: {ADLER_US_PCT}%")
print(f"  UK Percentage: {ADLER_UK_PCT}%")
print("\n" + "="*60)
print("Searching for surnames with similar statistics...")
print("="*60)

# We need actual census data to populate this
# For now, this script provides the framework for matching
