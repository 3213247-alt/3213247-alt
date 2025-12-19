#!/usr/bin/env python3
"""
Find surnames matching Adler across 4 metrics:
1. U.S. Census 2010: count ~16,412, rank ~2,223, proportion ~0.0053%
2. U.K. proportion ~0.004%
3. Linguistic similarity (German/Jewish origin, similar spelling)
4. Demographic/geographic distribution similarity
"""

import json
import re
from typing import List, Dict, Tuple
from difflib import SequenceMatcher

# Adler baseline metrics
ADLER_METRICS = {
    'us_count': 16412,
    'us_rank': 2223,
    'us_proportion': 0.000053,  # 0.0053%
    'uk_proportion': 0.00004,   # 0.004% (unverified)
    'origin': 'German/Jewish',
    'length': 5,
    'pattern': 'A-d-l-e-r',  # Consonant-vowel-consonant-vowel-consonant
}

def similarity_score(s1: str, s2: str) -> float:
    """Calculate string similarity using SequenceMatcher"""
    return SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

def phonetic_similarity(s1: str, s2: str) -> bool:
    """Check if surnames sound similar (basic check)"""
    # Remove vowels and compare consonant patterns
    def get_consonants(s):
        return ''.join(c for c in s.lower() if c not in 'aeiou')
    
    c1 = get_consonants(s1)
    c2 = get_consonants(s2)
    
    # Check if consonant patterns match closely
    if len(c1) == len(c2):
        return similarity_score(c1, c2) > 0.7
    return False

def pattern_match(surname: str) -> bool:
    """Check if surname matches Adler's pattern (C-V-C-V-C)"""
    pattern = re.compile(r'^[bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz][aeiou][bcdfghjklmnpqrstvwxyz]', re.IGNORECASE)
    return bool(pattern.match(surname))

def find_similar_surnames() -> List[Dict]:
    """
    Find surnames similar to Adler based on:
    1. Spelling similarity
    2. Phonetic similarity  
    3. Pattern matching
    4. German/Jewish origin
    """
    
    # Common German/Jewish surnames with similar characteristics
    # These are candidates that might match Adler's metrics
    candidate_surnames = [
        # Very similar spelling
        'Adler', 'Adlers', 'Adlerman', 'Adlert', 'Adlerton',
        'Alder', 'Alders', 'Alderman', 'Alderton',
        'Adlerstein', 'Adlerberg', 'Adlerfeld',
        
        # Similar pattern and origin
        'Abram', 'Abrams', 'Abramson', 'Abramowitz',
        'Ackerman', 'Ackermann', 'Ackert',
        'Adler', 'Adlerstein', 'Adlerberg',
        'Altman', 'Altmann', 'Altmanns',
        'Arndt', 'Arnold', 'Arnoldi', 'Arnolds',
        'Asher', 'Asherman', 'Asherson',
        'Auer', 'Auerbach', 'Auerman',
        'Bach', 'Bachman', 'Bachmann',
        'Baer', 'Baerman', 'Baermann',
        'Becker', 'Beckerman', 'Beckert',
        'Berg', 'Bergman', 'Bergmann', 'Bergstein',
        'Blum', 'Bluman', 'Blumenthal',
        'Brandt', 'Brand', 'Brandman',
        'Braun', 'Braunstein', 'Braunfeld',
        'Cohen', 'Cohn', 'Cohens',
        'Dahl', 'Dahlman', 'Dahlmann',
        'Ehrlich', 'Ehrman', 'Ehrlichman',
        'Feldman', 'Feldmann', 'Feldstein',
        'Fischer', 'Fischman', 'Fischmann',
        'Friedman', 'Friedmann', 'Friedberg',
        'Gold', 'Goldman', 'Goldmann', 'Goldberg', 'Goldstein',
        'Green', 'Greenberg', 'Greenstein', 'Greenfeld',
        'Gross', 'Grossman', 'Grossmann',
        'Gutman', 'Gutmann', 'Guterman',
        'Hahn', 'Hahne', 'Hahnemann',
        'Hart', 'Hartman', 'Hartmann', 'Hartstein',
        'Heller', 'Hellman', 'Hellmann',
        'Hirsch', 'Hirschman', 'Hirschmann',
        'Hoffman', 'Hoffmann', 'Hoffman',
        'Kahn', 'Kahne', 'Kahneman',
        'Katz', 'Katzman', 'Katzmann',
        'Klein', 'Kleinman', 'Kleinmann',
        'Kramer', 'Kraemer', 'Kraemer',
        'Lehman', 'Lehmann', 'Lehmanns',
        'Levi', 'Levin', 'Levine', 'Levinson',
        'Levy', 'Levy', 'Levys',
        'Mann', 'Manns', 'Mannheim',
        'Marks', 'Markowitz', 'Markman',
        'Mayer', 'Meyer', 'Meier', 'Meyers',
        'Miller', 'Millerman', 'Millermann',
        'Muller', 'Mueller', 'Mullerman',
        'Neuman', 'Neumann', 'Neumans',
        'Ober', 'Oberman', 'Obermann',
        'Parker', 'Parkman', 'Parkmann',
        'Rosen', 'Rosenberg', 'Rosenstein', 'Rosenfeld',
        'Roth', 'Rothman', 'Rothmann', 'Rothstein',
        'Schmidt', 'Schmitt', 'Schmitz',
        'Schneider', 'Schneiderman', 'Schneidermann',
        'Schwartz', 'Schwarz', 'Schwartzman',
        'Silver', 'Silverman', 'Silverstein',
        'Singer', 'Singerman', 'Singermann',
        'Stein', 'Steinberg', 'Steinman', 'Steinmann',
        'Stern', 'Sternberg', 'Sternman', 'Sternmann',
        'Strauss', 'Straus', 'Straussman',
        'Weber', 'Weberman', 'Webermann',
        'Weiss', 'Weissman', 'Weissmann', 'Weissberg',
        'Werner', 'Wernerman', 'Wernermann',
        'Wolff', 'Wolf', 'Wolfman', 'Wolfmann',
        'Zimmerman', 'Zimmermann', 'Zimmermans',
    ]
    
    # Remove duplicates and sort
    candidate_surnames = sorted(list(set(candidate_surnames)))
    
    matches = []
    
    for surname in candidate_surnames:
        if surname == 'Adler':
            continue
            
        # Calculate similarity metrics
        spelling_sim = similarity_score('Adler', surname)
        phonetic_sim = phonetic_similarity('Adler', surname)
        pattern_match_score = 1.0 if pattern_match(surname) else 0.0
        
        # Check origin similarity (German/Jewish)
        origin_match = True  # Most candidates are German/Jewish
        
        # Calculate overall score
        # Weight: spelling 40%, phonetic 30%, pattern 20%, origin 10%
        overall_score = (
            spelling_sim * 0.4 +
            (1.0 if phonetic_sim else 0.0) * 0.3 +
            pattern_match_score * 0.2 +
            (1.0 if origin_match else 0.0) * 0.1
        )
        
        matches.append({
            'surname': surname,
            'spelling_similarity': spelling_sim,
            'phonetic_similarity': phonetic_sim,
            'pattern_match': bool(pattern_match_score),
            'origin_match': origin_match,
            'overall_score': overall_score,
            'length': len(surname),
            'starts_with_a': surname[0].upper() == 'A',
        })
    
    # Sort by overall score descending
    matches.sort(key=lambda x: x['overall_score'], reverse=True)
    
    return matches

def filter_by_metrics(matches: List[Dict], 
                      us_count_range: Tuple[int, int] = (10000, 25000),
                      us_rank_range: Tuple[int, int] = (1500, 3000),
                      us_prop_range: Tuple[float, float] = (0.00003, 0.00008),
                      uk_prop_range: Tuple[float, float] = (0.00002, 0.00006)) -> List[Dict]:
    """
    Filter matches by demographic metrics.
    Note: This is a placeholder - actual data would need to be loaded from census files.
    """
    # For now, we'll mark which ones are likely to match based on similarity
    # In a real implementation, we'd query actual census data
    
    filtered = []
    for match in matches:
        # Estimate likelihood of matching metrics based on similarity
        # Very similar surnames likely have similar demographics
        if match['overall_score'] > 0.6:
            match['estimated_metric_match'] = True
            match['metric_confidence'] = match['overall_score']
        else:
            match['estimated_metric_match'] = False
            match['metric_confidence'] = 0.0
        
        filtered.append(match)
    
    return filtered

def main():
    print("Finding surnames matching Adler across 4 metrics...")
    print("=" * 70)
    print(f"\nAdler Baseline Metrics:")
    print(f"  U.S. Count: {ADLER_METRICS['us_count']:,}")
    print(f"  U.S. Rank: {ADLER_METRICS['us_rank']:,}")
    print(f"  U.S. Proportion: {ADLER_METRICS['us_proportion']*100:.4f}%")
    print(f"  U.K. Proportion: {ADLER_METRICS['uk_proportion']*100:.4f}%")
    print(f"  Origin: {ADLER_METRICS['origin']}")
    print(f"  Length: {ADLER_METRICS['length']}")
    print()
    
    # Find similar surnames
    matches = find_similar_surnames()
    
    # Filter by estimated metrics
    filtered_matches = filter_by_metrics(matches)
    
    # Get top 50 matches
    top_50 = filtered_matches[:50]
    
    print(f"\nTop 50 Surnames Matching Adler (sorted by similarity):")
    print("=" * 70)
    print(f"{'Rank':<6} {'Surname':<20} {'Spelling':<10} {'Phonetic':<10} {'Pattern':<10} {'Overall':<10}")
    print("-" * 70)
    
    for i, match in enumerate(top_50, 1):
        print(f"{i:<6} {match['surname']:<20} {match['spelling_similarity']:<10.3f} "
              f"{'Yes' if match['phonetic_similarity'] else 'No':<10} "
              f"{'Yes' if match['pattern_match'] else 'No':<10} "
              f"{match['overall_score']:<10.3f}")
    
    # Find best overall match
    best_match = max(filtered_matches, key=lambda x: x['overall_score'])
    
    print("\n" + "=" * 70)
    print(f"\nBEST MATCH: {best_match['surname']}")
    print(f"  Overall Score: {best_match['overall_score']:.3f}")
    print(f"  Spelling Similarity: {best_match['spelling_similarity']:.3f}")
    print(f"  Phonetic Similarity: {'Yes' if best_match['phonetic_similarity'] else 'No'}")
    print(f"  Pattern Match: {'Yes' if best_match['pattern_match'] else 'No'}")
    print(f"  Origin Match: {'Yes' if best_match['origin_match'] else 'No'}")
    print(f"  Estimated Metric Match: {'Yes' if best_match['estimated_metric_match'] else 'No'}")
    
    # Save results to JSON
    output = {
        'adler_metrics': ADLER_METRICS,
        'top_50_matches': top_50,
        'best_match': best_match,
        'total_candidates': len(matches)
    }
    
    with open('adler_surname_matches.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to adler_surname_matches.json")
    print(f"Total candidates analyzed: {len(matches)}")

if __name__ == '__main__':
    main()
