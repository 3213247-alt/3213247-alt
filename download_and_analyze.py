#!/usr/bin/env python3
"""
Download and analyze surname data to find matches for Adler.
"""

import csv
import gzip
import urllib.request
import io
from pathlib import Path
from adler_surname_matcher import SurnameMatcher, ADLER

def download_us_census_surnames():
    """
    Download U.S. Census 2010 surname data.
    The file is available from Census.gov
    """
    # U.S. Census 2010 surname file URL
    # Note: This is a large file (~2MB compressed)
    url = "https://www2.census.gov/topics/genealogy/2010surnames/names.zip"
    
    print("Attempting to download U.S. Census surname data...")
    print("Note: This may take a few minutes...")
    
    try:
        # Download the file
        response = urllib.request.urlopen(url, timeout=30)
        data = response.read()
        
        # Save to file
        with open('census_names.zip', 'wb') as f:
            f.write(data)
        
        print("Downloaded census_names.zip")
        print("Note: You may need to extract and process the file manually.")
        return True
    except Exception as e:
        print(f"Could not download: {e}")
        print("\nAlternative: Download manually from:")
        print("https://www2.census.gov/topics/genealogy/2010surnames/")
        return False


def create_sample_data_based_on_patterns():
    """
    Create sample surname data based on known patterns around Adler's rank.
    Surnames ranked around 2,223 would have counts around 16,000-17,000.
    """
    # Based on surname distribution patterns, surnames near rank 2,223
    # would have counts in the 15,000-18,000 range
    
    sample_surnames = []
    
    # These are example surnames that might be in similar range
    # Actual data needed for precision
    potential_matches = [
        # Surnames with similar characteristics to Adler (German/Jewish origin)
        # Rank range: 2000-2500, Count range: 15000-18000
    ]
    
    return sample_surnames


if __name__ == '__main__':
    print("Adler Surname Matching Tool")
    print("=" * 50)
    
    # Check if data file exists
    data_files = ['surnames.csv', 'us_surnames.csv', 'census_surnames.csv']
    found = False
    
    for df in data_files:
        if Path(df).exists():
            print(f"Found data file: {df}")
            found = True
            
            # Run analysis
            matcher = SurnameMatcher(ADLER)
            surnames = matcher.load_from_csv(df)
            matches = matcher.find_matches(surnames, top_n=50)
            matcher.print_results(matches)
            break
    
    if not found:
        print("No data file found.")
        print("\nTo proceed:")
        print("1. Download U.S. Census 2010 surname data")
        print("2. Obtain U.K. surname data")
        print("3. Create CSV file with columns: surname,us_count,us_rank,us_proportion,uk_proportion")
        print("4. Run this script again")
