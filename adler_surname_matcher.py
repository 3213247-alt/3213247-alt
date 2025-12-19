#!/usr/bin/env python3
"""
Comprehensive surname matcher for Adler metrics.
Finds surnames matching Adler across 4 metrics:
1. U.S. Census 2010 count (16,412)
2. U.S. Census 2010 rank (2,223)
3. U.S. proportion (0.0053%)
4. U.K. proportion (0.004%)
"""

import csv
import json
import math
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Adler's exact metrics
ADLER = {
    'name': 'Adler',
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 16,412 / 308,745,538
    'uk_proportion': 0.00004,   # 0.004% (unverified)
}

US_POPULATION_2010 = 308745538


class SurnameMatcher:
    def __init__(self, target_metrics: Dict):
        self.target = target_metrics
        self.matches = []
    
    def calculate_metric_distance(self, value: float, target: float, metric_type: str) -> float:
        """
        Calculate normalized distance for a metric.
        Returns value between 0 (perfect match) and higher (worse match).
        """
        if value is None or target is None:
            return float('inf')
        
        if target == 0:
            return float('inf')
        
        # Use relative difference (percentage difference)
        diff = abs(value - target)
        relative_diff = diff / target
        
        return relative_diff
    
    def calculate_composite_score(self, surname_data: Dict) -> Tuple[float, Dict]:
        """
        Calculate composite similarity score across all 4 metrics.
        Returns (score, details) where lower score = better match.
        """
        scores = {}
        total_score = 0.0
        factors = 0
        
        # Metric 1: U.S. Count
        if 'us_count' in surname_data and surname_data['us_count']:
            count = int(surname_data['us_count'])
            count_score = self.calculate_metric_distance(count, self.target['us_count'], 'count')
            scores['us_count'] = count_score
            total_score += count_score
            factors += 1
        
        # Metric 2: U.S. Rank
        if 'us_rank' in surname_data and surname_data['us_rank']:
            rank = int(surname_data['us_rank'])
            rank_score = self.calculate_metric_distance(rank, self.target['us_rank'], 'rank')
            scores['us_rank'] = rank_score
            total_score += rank_score
            factors += 1
        
        # Metric 3: U.S. Proportion
        us_prop = None
        if 'us_proportion' in surname_data and surname_data['us_proportion']:
            try:
                prop_str = str(surname_data['us_proportion']).replace('%', '').strip()
                us_prop = float(prop_str)
                if us_prop > 1:  # If given as percentage (e.g., 0.0053%)
                    us_prop = us_prop / 100
            except:
                pass
        
        # Calculate from count if proportion not provided
        if us_prop is None and 'us_count' in surname_data and surname_data['us_count']:
            try:
                count = int(surname_data['us_count'])
                us_prop = count / US_POPULATION_2010
            except:
                pass
        
        if us_prop is not None:
            prop_score = self.calculate_metric_distance(us_prop, self.target['us_proportion'], 'proportion')
            scores['us_proportion'] = prop_score
            total_score += prop_score
            factors += 1
        
        # Metric 4: U.K. Proportion
        uk_prop = None
        if 'uk_proportion' in surname_data and surname_data['uk_proportion']:
            try:
                prop_str = str(surname_data['uk_proportion']).replace('%', '').strip()
                uk_prop = float(prop_str)
                if uk_prop > 1:  # If given as percentage
                    uk_prop = uk_prop / 100
            except:
                pass
        
        if uk_prop is not None:
            uk_score = self.calculate_metric_distance(uk_prop, self.target['uk_proportion'], 'uk_proportion')
            scores['uk_proportion'] = uk_score
            total_score += uk_score
            factors += 1
        
        # Average score (lower is better)
        if factors > 0:
            avg_score = total_score / factors
        else:
            avg_score = float('inf')
        
        return avg_score, scores
    
    def load_from_csv(self, filepath: str) -> List[Dict]:
        """Load surname data from CSV file"""
        surnames = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    surname = row.get('surname', '').strip()
                    if not surname or surname.upper() == 'ADLER':
                        continue
                    
                    data = {}
                    for key in ['us_count', 'us_rank', 'us_proportion', 'uk_proportion']:
                        if key in row and row[key]:
                            data[key] = row[key]
                    
                    surnames.append({
                        'name': surname,
                        **data
                    })
        except Exception as e:
            print(f"Error loading CSV: {e}")
        
        return surnames
    
    def find_matches(self, surnames: List[Dict], top_n: int = 50) -> List[Tuple[str, Dict, float, Dict]]:
        """
        Find top N surnames matching Adler's metrics.
        Returns list of (name, data, score, score_details) tuples.
        """
        results = []
        
        for surname in surnames:
            name = surname.get('name', '')
            score, details = self.calculate_composite_score(surname)
            
            if score != float('inf'):
                results.append((name, surname, score, details))
        
        # Sort by score (lower is better)
        results.sort(key=lambda x: x[2])
        
        return results[:top_n]
    
    def print_results(self, matches: List[Tuple[str, Dict, float, Dict]]):
        """Print formatted results"""
        if not matches:
            print("No matches found.")
            return
        
        print(f"\n{'='*100}")
        print(f"TOP 50 SURNAMES MATCHING ADLER'S METRICS")
        print(f"{'='*100}\n")
        
        print(f"Target Metrics:")
        print(f"  U.S. Count: {self.target['us_count']:,}")
        print(f"  U.S. Rank: {self.target['us_rank']:,}")
        print(f"  U.S. Proportion: {self.target['us_proportion']*100:.4f}%")
        print(f"  U.K. Proportion: {self.target['uk_proportion']*100:.4f}%")
        print()
        
        header = f"{'Rank':<6} {'Surname':<20} {'US Count':<12} {'US Rank':<10} {'US %':<12} {'UK %':<12} {'Score':<10}"
        print(header)
        print("-" * len(header))
        
        for i, (name, data, score, details) in enumerate(matches, 1):
            us_count = data.get('us_count', 'N/A')
            us_rank = data.get('us_rank', 'N/A')
            
            # Format proportion
            us_prop = data.get('us_proportion', None)
            if us_prop is None and us_count != 'N/A':
                try:
                    us_prop = int(str(us_count).replace(',', '')) / US_POPULATION_2010
                except:
                    us_prop = None
            
            us_prop_str = f"{us_prop*100:.4f}%" if us_prop is not None else "N/A"
            
            uk_prop = data.get('uk_proportion', None)
            uk_prop_str = f"{uk_prop*100:.4f}%" if uk_prop is not None else "N/A"
            
            print(f"{i:<6} {name:<20} {str(us_count):<12} {str(us_rank):<10} {us_prop_str:<12} {uk_prop_str:<12} {score:.6f}")
        
        # Best match details
        best_name, best_data, best_score, best_details = matches[0]
        print(f"\n{'='*100}")
        print(f"BEST MATCH: {best_name}")
        print(f"Composite Score: {best_score:.6f} (lower = better match)")
        print(f"\nDetailed Metrics:")
        print(f"  U.S. Count: {best_data.get('us_count', 'N/A')} (target: {self.target['us_count']:,})")
        print(f"  U.S. Rank: {best_data.get('us_rank', 'N/A')} (target: {self.target['us_rank']:,})")
        print(f"  U.S. Proportion: {us_prop_str if 'us_proportion' in best_data else 'N/A'} (target: {self.target['us_proportion']*100:.4f}%)")
        print(f"  U.K. Proportion: {uk_prop_str if 'uk_proportion' in best_data else 'N/A'} (target: {self.target['uk_proportion']*100:.4f}%)")
        print(f"\nIndividual Metric Scores:")
        for metric, metric_score in best_details.items():
            print(f"  {metric}: {metric_score:.6f}")


def main():
    matcher = SurnameMatcher(ADLER)
    
    # Try to find data files
    data_files = [
        'surnames.csv',
        'us_surnames.csv',
        'surname_data.csv',
        'census_surnames.csv',
        'surnames_us_uk.csv',
    ]
    
    data_file = None
    for df in data_files:
        if Path(df).exists():
            data_file = df
            break
    
    if not data_file:
        print("No surname data file found.")
        print("\nExpected CSV format:")
        print("  surname,us_count,us_rank,us_proportion,uk_proportion")
        print("\nExample row:")
        print("  Smith,2442977,1,0.7918%,0.8234%")
        print("\nNote: us_proportion and uk_proportion can be percentages (e.g., 0.0053%) or decimals (e.g., 0.000053)")
        print("\nTo use this tool:")
        print("  1. Obtain U.S. Census 2010 surname data")
        print("  2. Obtain U.K. surname data")
        print("  3. Combine into CSV with columns: surname,us_count,us_rank,us_proportion,uk_proportion")
        print("  4. Run: python3 adler_surname_matcher.py")
        return
    
    print(f"Loading surname data from {data_file}...")
    surnames = matcher.load_from_csv(data_file)
    print(f"Loaded {len(surnames)} surnames.")
    
    print("Finding matches...")
    matches = matcher.find_matches(surnames, top_n=50)
    
    matcher.print_results(matches)


if __name__ == '__main__':
    main()
