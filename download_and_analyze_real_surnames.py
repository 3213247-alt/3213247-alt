#!/usr/bin/env python3
"""
Download and analyze real 2010 US Census surname data to find surnames matching Adler's metrics.
"""

import csv
import io
import math
import urllib.request
import zipfile
from typing import Dict, List, Tuple

# Adler's target metrics (2010 US Census + UK estimates)
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 0.0053% = 16,412 / 308,745,538
    'uk_proportion': 0.00004,   # 0.004% (unverified)
}

US_POPULATION_2010 = 308745538

# URLs for 2010 US Census surname data
CENSUS_SURNAME_URLS = [
    "https://www2.census.gov/topics/genealogy/2010surnames/names.zip",
    "https://www2.census.gov/topics/genealogy/2010surnames/Names_2010Census_Top1000.xlsx",
    "https://www2.census.gov/topics/genealogy/2010surnames/Names_2010Census_Top10000.xlsx",
]


def download_census_data(url: str, output_file: str) -> bool:
    """Download census data from URL."""
    try:
        print(f"Downloading from {url}...")
        urllib.request.urlretrieve(url, output_file)
        print(f"Downloaded to {output_file}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def extract_zip_and_find_csv(zip_path: str) -> str:
    """Extract zip file and find CSV file."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"Files in zip: {file_list}")
            
            # Look for CSV files
            csv_files = [f for f in file_list if f.endswith('.csv')]
            if csv_files:
                csv_file = csv_files[0]
                zip_ref.extract(csv_file, '/workspace/')
                return f'/workspace/{csv_file}'
            
            # Look for text files
            txt_files = [f for f in file_list if f.endswith('.txt')]
            if txt_files:
                txt_file = txt_files[0]
                zip_ref.extract(txt_file, '/workspace/')
                return f'/workspace/{txt_file}'
    except Exception as e:
        print(f"Error extracting zip: {e}")
    return None


def parse_census_csv(csv_path: str) -> List[Dict]:
    """Parse census CSV file and extract surname data."""
    surnames = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            
            # Common delimiters: comma, tab
            delimiter = ',' if ',' in sample else '\t'
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for row in reader:
                # Try different column name variations
                surname = None
                count = None
                rank = None
                
                # Common column name variations
                for key in row.keys():
                    key_lower = key.lower()
                    if 'name' in key_lower or 'surname' in key_lower:
                        surname = row[key].strip()
                    elif 'count' in key_lower or 'frequency' in key_lower or 'number' in key_lower:
                        try:
                            count = int(row[key].replace(',', ''))
                        except:
                            pass
                    elif 'rank' in key_lower:
                        try:
                            rank = int(row[key].replace(',', ''))
                        except:
                            pass
                
                if surname and count:
                    # Calculate proportion
                    proportion = count / US_POPULATION_2010
                    
                    surnames.append({
                        'surname': surname,
                        'us_count': count,
                        'us_rank': rank,
                        'us_proportion': proportion,
                        'uk_proportion': None  # Will need separate UK data
                    })
        
        print(f"Parsed {len(surnames)} surnames from {csv_path}")
        return surnames
        
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return []


def calculate_similarity_score(surname_data: Dict, target: Dict) -> float:
    """
    Calculate similarity score across all 4 metrics.
    Lower score = better match (closer to 0 = perfect match)
    """
    scores = []
    
    # Metric 1: US Count similarity (log scale for better matching)
    if surname_data.get('us_count'):
        count_diff = abs(math.log(surname_data['us_count'] + 1) - math.log(target['us_count'] + 1))
        count_score = count_diff / math.log(target['us_count'] + 1)  # Normalized
        scores.append(count_score)
    
    # Metric 2: US Rank similarity
    if surname_data.get('us_rank'):
        rank_diff = abs(surname_data['us_rank'] - target['us_rank'])
        rank_score = rank_diff / target['us_rank']  # Normalized
        scores.append(rank_score)
    
    # Metric 3: US Proportion similarity
    if surname_data.get('us_proportion'):
        prop_diff = abs(surname_data['us_proportion'] - target['us_proportion'])
        prop_score = prop_diff / target['us_proportion']  # Normalized
        scores.append(prop_score)
    elif surname_data.get('us_count'):
        # Calculate proportion from count
        calculated_prop = surname_data['us_count'] / US_POPULATION_2010
        prop_diff = abs(calculated_prop - target['us_proportion'])
        prop_score = prop_diff / target['us_proportion']
        scores.append(prop_score)
    
    # Metric 4: UK Proportion similarity (only if available)
    if surname_data.get('uk_proportion') is not None:
        uk_diff = abs(surname_data['uk_proportion'] - target['uk_proportion'])
        uk_score = uk_diff / target['uk_proportion']  # Normalized
        scores.append(uk_score)
    
    # Return average of all available metrics
    if len(scores) == 0:
        return float('inf')
    
    return sum(scores) / len(scores)


def find_matching_surnames(surname_database: List[Dict], target: Dict, top_n: int = 50, exclude_surname: str = None) -> List[Tuple[str, float, Dict]]:
    """
    Find surnames matching target metrics.
    Returns list of (surname, similarity_score, data) tuples, sorted by similarity.
    
    Args:
        exclude_surname: Surname to exclude from results (e.g., 'Adler' when finding matches for Adler)
    """
    matches = []
    
    for surname_entry in surname_database:
        surname_name = surname_entry.get('surname', '')
        if not surname_name:
            continue
        
        # Exclude the target surname itself
        if exclude_surname and surname_name.upper() == exclude_surname.upper():
            continue
            
        similarity = calculate_similarity_score(surname_entry, target)
        
        matches.append((surname_name, similarity, surname_entry))
    
    # Sort by similarity (lower is better)
    matches.sort(key=lambda x: x[1])
    
    return matches[:top_n]


def main():
    """Main function to download and analyze real census data."""
    print("=" * 80)
    print("REAL 2010 US CENSUS SURNAME DATA ANALYSIS")
    print("Finding surnames matching Adler's metrics")
    print("=" * 80)
    print()
    
    print("Target Metrics (Adler):")
    print(f"  US Count:     {ADLER_METRICS['us_count']:,}")
    print(f"  US Rank:      {ADLER_METRICS['us_rank']:,}")
    print(f"  US Proportion: {ADLER_METRICS['us_proportion']:.6f} ({ADLER_METRICS['us_proportion']*100:.4f}%)")
    print(f"  UK Proportion: {ADLER_METRICS['uk_proportion']:.6f} ({ADLER_METRICS['uk_proportion']*100:.4f}%)")
    print()
    
    # Try to download census data
    zip_path = '/workspace/census_names.zip'
    csv_path = None
    
    # Try downloading the zip file
    if download_census_data(CENSUS_SURNAME_URLS[0], zip_path):
        csv_path = extract_zip_and_find_csv(zip_path)
    
    # If zip didn't work, try alternative approaches
    if not csv_path:
        print("\nTrying alternative data sources...")
        # Try direct CSV download
        csv_url = "https://www2.census.gov/topics/genealogy/2010surnames/Names_2010Census_Top1000.csv"
        csv_path = '/workspace/census_names.csv'
        if download_census_data(csv_url, csv_path):
            pass
        else:
            print("Could not download census data. Trying local file search...")
            # Check if file already exists
            import os
            if os.path.exists('/workspace/census_names.csv'):
                csv_path = '/workspace/census_names.csv'
            elif os.path.exists('/workspace/Names_2010Census_Top1000.csv'):
                csv_path = '/workspace/Names_2010Census_Top1000.csv'
    
    if not csv_path:
        print("\nERROR: Could not obtain census data file.")
        print("Please ensure census data is available or manually download it.")
        return
    
    # Parse the census data
    print(f"\nParsing census data from {csv_path}...")
    surnames = parse_census_csv(csv_path)
    
    if not surnames:
        print("ERROR: Could not parse any surnames from the data file.")
        print("Trying alternative parsing methods...")
        # Try reading as text file
        try:
            with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[:100]  # First 100 lines
                print("First few lines of file:")
                for i, line in enumerate(lines[:10]):
                    print(f"  {i+1}: {line[:100]}")
        except Exception as e:
            print(f"Error reading file: {e}")
        return
    
    print(f"\nLoaded {len(surnames)} surnames from census data")
    
    # Find matches (excluding Adler itself)
    print("\nFinding surnames matching all 4 metrics (excluding Adler)...")
    matches = find_matching_surnames(surnames, ADLER_METRICS, top_n=50, exclude_surname='Adler')
    
    if not matches:
        print("No matches found. Showing closest matches anyway...")
        # Show all surnames sorted by count similarity
        all_sorted = sorted(surnames, key=lambda x: abs(x.get('us_count', 0) - ADLER_METRICS['us_count']))
        matches = [(s['surname'], calculate_similarity_score(s, ADLER_METRICS), s) for s in all_sorted[:50]]
        matches.sort(key=lambda x: x[1])
    
    # Display top 50 matches
    print("\n" + "=" * 100)
    print("TOP 50 REAL SURNAMES MATCHING ADLER'S METRICS")
    print("=" * 100)
    print()
    print(f"{'Rank':<6} {'Surname':<20} {'US Count':<12} {'US Rank':<12} {'US %':<12} {'UK %':<12} {'Score':<10}")
    print("-" * 100)
    
    for idx, (surname, score, data) in enumerate(matches, 1):
        us_count = data.get('us_count', 'N/A')
        us_rank = data.get('us_rank', 'N/A')
        us_prop = data.get('us_proportion', 0)
        uk_prop = data.get('uk_proportion', 'N/A')
        
        if us_prop == 0 and us_count != 'N/A':
            us_prop = us_count / US_POPULATION_2010
        
        uk_display = f"{uk_prop*100:.4f}%" if isinstance(uk_prop, (int, float)) else str(uk_prop)
        
        print(f"{idx:<6} {surname:<20} {str(us_count):<12} {str(us_rank):<12} "
              f"{us_prop*100:.4f}%{'':<6} {uk_display:<12} {score:.6f}")
    
    print()
    print("=" * 100)
    print("BEST MATCH (Lowest Score = Best Match)")
    print("=" * 100)
    
    if matches:
        best_surname, best_score, best_data = matches[0]
        print(f"Surname: {best_surname}")
        print(f"Similarity Score: {best_score:.6f} (lower = better)")
        print()
        print("Metrics:")
        print(f"  US Count:     {best_data.get('us_count', 'N/A'):,}")
        print(f"  US Rank:      {best_data.get('us_rank', 'N/A'):,}")
        print(f"  US Proportion: {best_data.get('us_proportion', 0):.6f} ({best_data.get('us_proportion', 0)*100:.4f}%)")
        uk_prop = best_data.get('uk_proportion', 'N/A')
        if isinstance(uk_prop, (int, float)):
            print(f"  UK Proportion: {uk_prop:.6f} ({uk_prop*100:.4f}%)")
        else:
            print(f"  UK Proportion: {uk_prop} (not available in census data)")
        print()
        print("Comparison to Adler:")
        print(f"  Count difference:  {abs(best_data.get('us_count', 0) - ADLER_METRICS['us_count']):,}")
        if best_data.get('us_rank'):
            print(f"  Rank difference:   {abs(best_data.get('us_rank', 0) - ADLER_METRICS['us_rank']):,}")
        print(f"  US % difference:   {abs(best_data.get('us_proportion', 0) - ADLER_METRICS['us_proportion']):.8f}")
    
    print()
    print("=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    print("\nNOTE: UK proportion data is not included in US Census data.")
    print("To get complete matches, UK surname data would need to be obtained separately.")


if __name__ == '__main__':
    main()
