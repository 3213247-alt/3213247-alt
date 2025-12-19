# Adler Surname Metric Matching

## Objective
Find surnames that match Adler's metrics across 4 dimensions:
1. **U.S. Census 2010 count**: 16,412
2. **U.S. Census 2010 rank**: 2,223
3. **U.S. proportion**: 0.0053% (16,412 / 308,745,538)
4. **U.K. proportion**: 0.004% (unverified)

## Target Metrics
- **U.S. Count**: 16,412
- **U.S. Rank**: 2,223
- **U.S. Proportion**: 0.000053 (0.0053%)
- **U.K. Proportion**: 0.00004 (0.004%)

## Data Sources Needed
1. **U.S. Census 2010 Surname File**: Contains all surnames with counts and ranks
2. **U.K. Surname Data**: Official or reliable source for U.K. surname proportions

## Matching Algorithm
The matching algorithm calculates a composite similarity score:
- For each metric, calculates normalized distance: `|value - target| / target`
- Averages all available metrics
- Lower score = better match (closer to 0)

## Usage
```bash
python3 adler_surname_matcher.py
```

## Expected Output
1. List of 50 surnames closest to Adler's metrics
2. Best match identified with detailed comparison
3. Individual metric scores for each surname

## Data File Format
CSV with columns:
- `surname`: Surname name
- `us_count`: U.S. Census 2010 count
- `us_rank`: U.S. Census 2010 rank
- `us_proportion`: U.S. proportion (as decimal or percentage)
- `uk_proportion`: U.K. proportion (as decimal or percentage)
