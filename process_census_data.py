#!/usr/bin/env python3
"""
Process U.S. Census 2010 surname data to find surnames matching Adler's metrics.
"""

import csv
import math

# Adler's exact metrics
ADLER = {
    'name': 'ADLER',
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 16412 / 308745538,  # 0.00005318
    'prop100k': 5.56,  # per 100k
}

US_POPULATION_2010 = 308745538


def calculate_similarity(surname_data, target):
    """Calculate composite similarity score (lower = better match)"""
    scores = []
    
    # Metric 1: Count similarity
    count_diff = abs(surname_data['count'] - target['us_count'])
    count_score = count_diff / target['us_count']
    scores.append(count_score)
    
    # Metric 2: Rank similarity
    rank_diff = abs(surname_data['rank'] - target['us_rank'])
    rank_score = rank_diff / target['us_rank']
    scores.append(rank_score)
    
    # Metric 3: Proportion similarity (from prop100k)
    prop100k_diff = abs(surname_data['prop100k'] - target['prop100k'])
    prop100k_score = prop100k_diff / target['prop100k']
    scores.append(prop100k_score)
    
    # Average score
    return sum(scores) / len(scores)


def load_census_data(filename):
    """Load and parse Census surname data"""
    surnames = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].strip().upper()
            if name == 'ADLER':
                continue
            
            try:
                rank = int(row['rank'])
                count = int(row['count'])
                prop100k = float(row['prop100k'])
                
                # Calculate proportion
                proportion = count / US_POPULATION_2010
                
                surnames.append({
                    'name': name,
                    'rank': rank,
                    'count': count,
                    'prop100k': prop100k,
                    'proportion': proportion,
                })
            except (ValueError, KeyError) as e:
                continue
    
    return surnames


def find_matches(surnames, target, top_n=50):
    """Find top N surnames matching target metrics"""
    matches = []
    
    for surname in surnames:
        # Only consider surnames in similar range
        # Rank: within 500 positions (1723-2723)
        # Count: within 30% (11500-21300)
        if (abs(surname['rank'] - target['us_rank']) <= 500 and
            abs(surname['count'] - target['us_count']) / target['us_count'] <= 0.3):
            
            score = calculate_similarity(surname, target)
            matches.append((surname, score))
    
    # Sort by score
    matches.sort(key=lambda x: x[1])
    
    return matches[:top_n]


def main():
    print("Processing U.S. Census 2010 surname data...")
    print(f"Target: Adler - Rank {ADLER['us_rank']}, Count {ADLER['us_count']:,}, Prop100k {ADLER['prop100k']}")
    print()
    
    surnames = load_census_data('Names_2010Census.csv')
    print(f"Loaded {len(surnames):,} surnames from Census data")
    
    matches = find_matches(surnames, ADLER, top_n=50)
    
    print(f"\n{'='*100}")
    print(f"TOP 50 SURNAMES MATCHING ADLER'S METRICS (U.S. DATA)")
    print(f"{'='*100}\n")
    
    print(f"{'Rank':<6} {'Surname':<20} {'US Count':<12} {'US Rank':<10} {'Prop100k':<12} {'US %':<12} {'Score':<10}")
    print("-" * 100)
    
    for i, (surname, score) in enumerate(matches, 1):
        print(f"{i:<6} {surname['name']:<20} {surname['count']:>11,} {surname['rank']:>9,} "
              f"{surname['prop100k']:>11.2f} {surname['proportion']*100:>11.6f}% {score:>9.6f}")
    
    # Best match
    if matches:
        best_surname, best_score = matches[0]
        print(f"\n{'='*100}")
        print(f"BEST MATCH: {best_surname['name']}")
        print(f"Composite Score: {best_score:.6f} (lower = better match)")
        print(f"\nDetailed Comparison:")
        print(f"  U.S. Count: {best_surname['count']:,} (Adler: {ADLER['us_count']:,}, diff: {abs(best_surname['count'] - ADLER['us_count']):,})")
        print(f"  U.S. Rank: {best_surname['rank']:,} (Adler: {ADLER['us_rank']:,}, diff: {abs(best_surname['rank'] - ADLER['us_rank']):,})")
        print(f"  Prop100k: {best_surname['prop100k']:.2f} (Adler: {ADLER['prop100k']:.2f}, diff: {abs(best_surname['prop100k'] - ADLER['prop100k']):.2f})")
        print(f"  U.S. Proportion: {best_surname['proportion']*100:.6f}% (Adler: {ADLER['us_proportion']*100:.6f}%)")
        
        # Calculate individual metric scores
        count_diff_pct = abs(best_surname['count'] - ADLER['us_count']) / ADLER['us_count'] * 100
        rank_diff_pct = abs(best_surname['rank'] - ADLER['us_rank']) / ADLER['us_rank'] * 100
        prop_diff_pct = abs(best_surname['prop100k'] - ADLER['prop100k']) / ADLER['prop100k'] * 100
        
        print(f"\nIndividual Metric Differences:")
        print(f"  Count: {count_diff_pct:.2f}% difference")
        print(f"  Rank: {rank_diff_pct:.2f}% difference")
        print(f"  Prop100k: {prop_diff_pct:.2f}% difference")
        
        print(f"\nNote: U.K. proportion data not available in Census file.")
        print(f"      For complete 4-metric matching, U.K. surname data needed.")


if __name__ == '__main__':
    main()
