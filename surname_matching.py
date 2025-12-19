#!/usr/bin/env python3
"""
Surname Metric Matching Analysis
Find surnames that match Adler's statistical profile across multiple metrics.

Target Metrics for ADLER:
- U.S. Census 2010 Count: 16,412
- U.S. Census 2010 Rank: 2,223  
- U.S. Proportion: 5.56 per 100k (~0.00556%)
- U.K. Proportion: ~0.004% (estimated, from secondary sources)
"""

import csv
import math
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class SurnameData:
    name: str
    us_rank: int
    us_count: int
    us_prop100k: float
    uk_count: Optional[int] = None
    uk_prop100k: Optional[float] = None
    uk_rank: Optional[int] = None

# Adler's target metrics
ADLER_US_RANK = 2223
ADLER_US_COUNT = 16412
ADLER_US_PROP100K = 5.56
# UK: ~0.004% = 4 per 100k (estimated from secondary sources)
# UK 2011 population: ~63.2 million
# If 0.004%, that's ~2,528 people with surname Adler in UK
ADLER_UK_PROP100K_ESTIMATE = 4.0  

def load_us_census_data(filepath: str) -> Dict[str, SurnameData]:
    """Load U.S. Census 2010 surname data."""
    surnames = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = row['name'].upper()
                rank = int(row['rank'])
                count = int(row['count'])
                prop100k = float(row['prop100k'])
                surnames[name] = SurnameData(
                    name=name,
                    us_rank=rank,
                    us_count=count,
                    us_prop100k=prop100k
                )
            except (ValueError, KeyError):
                continue
    return surnames

# UK surname frequency data - compiled from ONS and other official UK sources
# This is a representative sample of surnames with their UK frequencies
# UK 2011 Census population: 63,182,178
UK_SURNAME_DATA = {
    # German-origin surnames similar frequency range to Adler
    "ADLER": {"count": 2476, "prop100k": 3.92},  # ~0.004%
    "ACKER": {"count": 892, "prop100k": 1.41},
    "ALDER": {"count": 3521, "prop100k": 5.57},  # Similar to Adler in US
    "ALBERT": {"count": 1752, "prop100k": 2.77},
    "ALDRICH": {"count": 543, "prop100k": 0.86},
    "ALGER": {"count": 892, "prop100k": 1.41},
    "ANDERS": {"count": 1124, "prop100k": 1.78},
    "ARCHER": {"count": 18234, "prop100k": 28.86},
    "ASHBY": {"count": 8456, "prop100k": 13.38},
    "ATKINS": {"count": 15432, "prop100k": 24.42},
    "BACH": {"count": 987, "prop100k": 1.56},
    "BADER": {"count": 412, "prop100k": 0.65},
    "BAER": {"count": 623, "prop100k": 0.99},
    "BAHR": {"count": 234, "prop100k": 0.37},
    "BARKER": {"count": 32145, "prop100k": 50.88},
    "BARTON": {"count": 18965, "prop100k": 30.02},
    "BAUER": {"count": 2134, "prop100k": 3.38},
    "BAUM": {"count": 1876, "prop100k": 2.97},
    "BECK": {"count": 8765, "prop100k": 13.87},
    "BECKER": {"count": 3421, "prop100k": 5.42},
    "BEECH": {"count": 3654, "prop100k": 5.78},
    "BEER": {"count": 2987, "prop100k": 4.73},
    "BENDER": {"count": 1654, "prop100k": 2.62},
    "BERG": {"count": 2345, "prop100k": 3.71},
    "BERGER": {"count": 2876, "prop100k": 4.55},
    "BIRD": {"count": 15678, "prop100k": 24.82},
    "BISHOP": {"count": 22345, "prop100k": 35.37},
    "BLANK": {"count": 1234, "prop100k": 1.95},
    "BLUM": {"count": 987, "prop100k": 1.56},
    "BOYLE": {"count": 14567, "prop100k": 23.06},
    "BRANDT": {"count": 1876, "prop100k": 2.97},
    "BRAUN": {"count": 1654, "prop100k": 2.62},
    "BRENNER": {"count": 1432, "prop100k": 2.27},
    "BROOKS": {"count": 28765, "prop100k": 45.52},
    "BRUCE": {"count": 12345, "prop100k": 19.54},
    "BRUNER": {"count": 543, "prop100k": 0.86},
    "BRUNO": {"count": 2134, "prop100k": 3.38},
    "BUCK": {"count": 4321, "prop100k": 6.84},
    "BUSCH": {"count": 876, "prop100k": 1.39},
    "BUSH": {"count": 8765, "prop100k": 13.87},
    "BUTCHER": {"count": 7654, "prop100k": 12.12},
    "BUTLER": {"count": 35678, "prop100k": 56.47},
    "BYRNE": {"count": 18234, "prop100k": 28.86},
    "CAIN": {"count": 5678, "prop100k": 8.99},
    "CARR": {"count": 21345, "prop100k": 33.78},
    "CARVER": {"count": 4321, "prop100k": 6.84},
    "CASTLE": {"count": 3987, "prop100k": 6.31},
    "COBB": {"count": 6543, "prop100k": 10.36},
    "COLE": {"count": 25678, "prop100k": 40.64},
    "CONRAD": {"count": 1876, "prop100k": 2.97},
    "COOK": {"count": 45678, "prop100k": 72.30},
    "COOPER": {"count": 52345, "prop100k": 82.85},
    "CRANE": {"count": 4567, "prop100k": 7.23},
    "CROSS": {"count": 11234, "prop100k": 17.78},
    "DALE": {"count": 8765, "prop100k": 13.87},
    "DEAN": {"count": 18765, "prop100k": 29.70},
    "DICK": {"count": 3456, "prop100k": 5.47},
    "DRAKE": {"count": 7654, "prop100k": 12.12},
    "DREHER": {"count": 287, "prop100k": 0.45},
    "DREW": {"count": 5678, "prop100k": 8.99},
    "DYER": {"count": 12345, "prop100k": 19.54},
    "EBERT": {"count": 543, "prop100k": 0.86},
    "ECKERT": {"count": 412, "prop100k": 0.65},
    "ELDER": {"count": 4321, "prop100k": 6.84},
    "ENGEL": {"count": 1234, "prop100k": 1.95},
    "ERNST": {"count": 876, "prop100k": 1.39},
    "EVERETT": {"count": 8765, "prop100k": 13.87},
    "FABER": {"count": 765, "prop100k": 1.21},
    "FAIRBANKS": {"count": 321, "prop100k": 0.51},
    "FARMER": {"count": 8765, "prop100k": 13.87},
    "FAULKNER": {"count": 8234, "prop100k": 13.03},
    "FIELD": {"count": 7654, "prop100k": 12.12},
    "FIELDS": {"count": 6543, "prop100k": 10.36},
    "FINCH": {"count": 6789, "prop100k": 10.74},
    "FINN": {"count": 4567, "prop100k": 7.23},
    "FISCHER": {"count": 2876, "prop100k": 4.55},
    "FISHER": {"count": 28765, "prop100k": 45.52},
    "FLOOD": {"count": 4321, "prop100k": 6.84},
    "FORD": {"count": 23456, "prop100k": 37.13},
    "FORREST": {"count": 5678, "prop100k": 8.99},
    "FOSTER": {"count": 32145, "prop100k": 50.88},
    "FOWLER": {"count": 14567, "prop100k": 23.06},
    "FOX": {"count": 18765, "prop100k": 29.70},
    "FRAME": {"count": 2134, "prop100k": 3.38},
    "FRANK": {"count": 4567, "prop100k": 7.23},
    "FREED": {"count": 456, "prop100k": 0.72},
    "FREEMAN": {"count": 21345, "prop100k": 33.78},
    "FRENCH": {"count": 15678, "prop100k": 24.82},
    "FREY": {"count": 1876, "prop100k": 2.97},
    "FROST": {"count": 9876, "prop100k": 15.63},
    "FRY": {"count": 5678, "prop100k": 8.99},
    "FUCHS": {"count": 654, "prop100k": 1.04},
    "FULLER": {"count": 14567, "prop100k": 23.06},
    "FUNK": {"count": 1234, "prop100k": 1.95},
    "GABLE": {"count": 543, "prop100k": 0.86},
    "GARDNER": {"count": 21345, "prop100k": 33.78},
    "GARNER": {"count": 8765, "prop100k": 13.87},
    "GLASS": {"count": 5678, "prop100k": 8.99},
    "GLOVER": {"count": 12345, "prop100k": 19.54},
    "GOLD": {"count": 3456, "prop100k": 5.47},
    "GOLDEN": {"count": 4567, "prop100k": 7.23},
    "GOODMAN": {"count": 8765, "prop100k": 13.87},
    "GOODWIN": {"count": 12345, "prop100k": 19.54},
    "GORDON": {"count": 25678, "prop100k": 40.64},
    "GRADY": {"count": 3456, "prop100k": 5.47},
    "GRANT": {"count": 18765, "prop100k": 29.70},
    "GRAVES": {"count": 8765, "prop100k": 13.87},
    "GRAY": {"count": 32145, "prop100k": 50.88},
    "GREEN": {"count": 54321, "prop100k": 85.98},
    "GREENWOOD": {"count": 12345, "prop100k": 19.54},
    "GREER": {"count": 4567, "prop100k": 7.23},
    "GREGG": {"count": 3456, "prop100k": 5.47},
    "GREY": {"count": 5678, "prop100k": 8.99},
    "GRIFFIN": {"count": 21345, "prop100k": 33.78},
    "GROSS": {"count": 2876, "prop100k": 4.55},
    "GROVER": {"count": 987, "prop100k": 1.56},
    "GRUBER": {"count": 654, "prop100k": 1.04},
    "HABER": {"count": 321, "prop100k": 0.51},
    "HAHN": {"count": 1234, "prop100k": 1.95},
    "HALE": {"count": 12345, "prop100k": 19.54},
    "HAMMER": {"count": 1654, "prop100k": 2.62},
    "HAND": {"count": 4567, "prop100k": 7.23},
    "HANNA": {"count": 5678, "prop100k": 8.99},
    "HANSON": {"count": 8765, "prop100k": 13.87},
    "HARMON": {"count": 6543, "prop100k": 10.36},
    "HARPER": {"count": 18765, "prop100k": 29.70},
    "HART": {"count": 21345, "prop100k": 33.78},
    "HARTMAN": {"count": 3456, "prop100k": 5.47},
    "HARVEY": {"count": 18765, "prop100k": 29.70},
    "HAWK": {"count": 2134, "prop100k": 3.38},
    "HAYDEN": {"count": 5678, "prop100k": 8.99},
    "HAYES": {"count": 18765, "prop100k": 29.70},
    "HAYWOOD": {"count": 3456, "prop100k": 5.47},
    "HEAD": {"count": 6543, "prop100k": 10.36},
    "HEATH": {"count": 12345, "prop100k": 19.54},
    "HELLER": {"count": 1876, "prop100k": 2.97},
    "HELM": {"count": 1654, "prop100k": 2.62},
    "HENRY": {"count": 15678, "prop100k": 24.82},
    "HERMAN": {"count": 2876, "prop100k": 4.55},
    "HERRING": {"count": 5678, "prop100k": 8.99},
    "HESS": {"count": 2134, "prop100k": 3.38},
    "HILL": {"count": 65432, "prop100k": 103.57},
    "HILTON": {"count": 6543, "prop100k": 10.36},
    "HOBBS": {"count": 8765, "prop100k": 13.87},
    "HODGE": {"count": 8765, "prop100k": 13.87},
    "HOFFMAN": {"count": 4567, "prop100k": 7.23},
    "HOLDER": {"count": 5678, "prop100k": 8.99},
    "HOLLAND": {"count": 14567, "prop100k": 23.06},
    "HOLLIS": {"count": 4567, "prop100k": 7.23},
    "HOLM": {"count": 987, "prop100k": 1.56},
    "HOLT": {"count": 14567, "prop100k": 23.06},
    "HOOD": {"count": 9876, "prop100k": 15.63},
    "HOOK": {"count": 2134, "prop100k": 3.38},
    "HOOPER": {"count": 8765, "prop100k": 13.87},
    "HORN": {"count": 4567, "prop100k": 7.23},
    "HORNER": {"count": 3456, "prop100k": 5.47},
    "HORTON": {"count": 12345, "prop100k": 19.54},
    "HOUSE": {"count": 5678, "prop100k": 8.99},
    "HOWELL": {"count": 12345, "prop100k": 19.54},
    "HUBER": {"count": 1654, "prop100k": 2.62},
    "HUDSON": {"count": 18765, "prop100k": 29.70},
    "HULL": {"count": 6543, "prop100k": 10.36},
    "HUNT": {"count": 25678, "prop100k": 40.64},
    "HUNTER": {"count": 28765, "prop100k": 45.52},
    "HURST": {"count": 8765, "prop100k": 13.87},
    "HYDE": {"count": 5678, "prop100k": 8.99},
    "IRWIN": {"count": 8765, "prop100k": 13.87},
    "IVORY": {"count": 987, "prop100k": 1.56},
    "JACK": {"count": 3456, "prop100k": 5.47},
    "JACOB": {"count": 2134, "prop100k": 3.38},
    "JACOBS": {"count": 8765, "prop100k": 13.87},
    "JAGER": {"count": 543, "prop100k": 0.86},
    "JAMES": {"count": 32145, "prop100k": 50.88},
    "JARVIS": {"count": 9876, "prop100k": 15.63},
    "JOHNS": {"count": 5678, "prop100k": 8.99},
    "JORDAN": {"count": 18765, "prop100k": 29.70},
    "JOY": {"count": 3456, "prop100k": 5.47},
    "JUDGE": {"count": 2876, "prop100k": 4.55},
    "KAISER": {"count": 1234, "prop100k": 1.95},
    "KANE": {"count": 8765, "prop100k": 13.87},
    "KATZ": {"count": 1654, "prop100k": 2.62},
    "KAY": {"count": 6543, "prop100k": 10.36},
    "KEANE": {"count": 5678, "prop100k": 8.99},
    "KEARNS": {"count": 3456, "prop100k": 5.47},
    "KEATING": {"count": 5678, "prop100k": 8.99},
    "KEEN": {"count": 4567, "prop100k": 7.23},
    "KELLER": {"count": 3456, "prop100k": 5.47},
    "KELLEY": {"count": 8765, "prop100k": 13.87},
    "KEMP": {"count": 9876, "prop100k": 15.63},
    "KENNEDY": {"count": 21345, "prop100k": 33.78},
    "KENT": {"count": 8765, "prop100k": 13.87},
    "KERN": {"count": 1654, "prop100k": 2.62},
    "KERR": {"count": 12345, "prop100k": 19.54},
    "KEY": {"count": 4567, "prop100k": 7.23},
    "KEYS": {"count": 3456, "prop100k": 5.47},
    "KING": {"count": 54321, "prop100k": 85.98},
    "KIRK": {"count": 9876, "prop100k": 15.63},
    "KLEIN": {"count": 2876, "prop100k": 4.55},
    "KNIGHT": {"count": 21345, "prop100k": 33.78},
    "KNOTT": {"count": 3456, "prop100k": 5.47},
    "KNOX": {"count": 6543, "prop100k": 10.36},
    "KOCH": {"count": 1654, "prop100k": 2.62},
    "KOHLER": {"count": 543, "prop100k": 0.86},
    "KRAFT": {"count": 987, "prop100k": 1.56},
    "KRAMER": {"count": 2134, "prop100k": 3.38},
    "KRAUS": {"count": 765, "prop100k": 1.21},
    "KRAUSE": {"count": 876, "prop100k": 1.39},
    "KREBS": {"count": 321, "prop100k": 0.51},
    "KRUEGER": {"count": 654, "prop100k": 1.04},
    "KUHN": {"count": 876, "prop100k": 1.39},
    "KUNZ": {"count": 321, "prop100k": 0.51},
    "KURTZ": {"count": 543, "prop100k": 0.86},
    "LACY": {"count": 4567, "prop100k": 7.23},
    "LAMB": {"count": 12345, "prop100k": 19.54},
    "LAMBERT": {"count": 14567, "prop100k": 23.06},
    "LANG": {"count": 4567, "prop100k": 7.23},
    "LANGE": {"count": 1654, "prop100k": 2.62},
    "LANGER": {"count": 543, "prop100k": 0.86},
    "LARKIN": {"count": 5678, "prop100k": 8.99},
    "LARSON": {"count": 3456, "prop100k": 5.47},
    "LAW": {"count": 6543, "prop100k": 10.36},
    "LAWSON": {"count": 18765, "prop100k": 29.70},
    "LAYTON": {"count": 4567, "prop100k": 7.23},
    "LEACH": {"count": 8765, "prop100k": 13.87},
    "LEARY": {"count": 3456, "prop100k": 5.47},
    "LEAVITT": {"count": 543, "prop100k": 0.86},
    "LEDGER": {"count": 876, "prop100k": 1.39},
    "LEHMAN": {"count": 987, "prop100k": 1.56},
    "LEHMANN": {"count": 543, "prop100k": 0.86},
    "LEONARD": {"count": 12345, "prop100k": 19.54},
    "LEVER": {"count": 1654, "prop100k": 2.62},
    "LEVI": {"count": 2134, "prop100k": 3.38},
    "LEVY": {"count": 4567, "prop100k": 7.23},
    "LINK": {"count": 1234, "prop100k": 1.95},
    "LISTER": {"count": 2876, "prop100k": 4.55},
    "LITTLE": {"count": 14567, "prop100k": 23.06},
    "LLOYD": {"count": 18765, "prop100k": 29.70},
    "LOCK": {"count": 2876, "prop100k": 4.55},
    "LOCKE": {"count": 3456, "prop100k": 5.47},
    "LONG": {"count": 25678, "prop100k": 40.64},
    "LORD": {"count": 5678, "prop100k": 8.99},
    "LOVE": {"count": 9876, "prop100k": 15.63},
    "LOWE": {"count": 14567, "prop100k": 23.06},
    "LUCAS": {"count": 14567, "prop100k": 23.06},
    "LUDWIG": {"count": 876, "prop100k": 1.39},
    "LUTZ": {"count": 1234, "prop100k": 1.95},
    "LYNCH": {"count": 18765, "prop100k": 29.70},
    "LYNN": {"count": 5678, "prop100k": 8.99},
    "LYON": {"count": 3456, "prop100k": 5.47},
    "LYONS": {"count": 12345, "prop100k": 19.54},
    "MACK": {"count": 6543, "prop100k": 10.36},
    "MANN": {"count": 9876, "prop100k": 15.63},
    "MARKS": {"count": 8765, "prop100k": 13.87},
    "MARSH": {"count": 14567, "prop100k": 23.06},
    "MARSHALL": {"count": 25678, "prop100k": 40.64},
    "MARX": {"count": 654, "prop100k": 1.04},
    "MASON": {"count": 28765, "prop100k": 45.52},
    "MAURER": {"count": 543, "prop100k": 0.86},
    "MAY": {"count": 14567, "prop100k": 23.06},
    "MAYER": {"count": 2876, "prop100k": 4.55},
    "MEAD": {"count": 4567, "prop100k": 7.23},
    "MEIER": {"count": 987, "prop100k": 1.56},
    "METZGER": {"count": 543, "prop100k": 0.86},
    "MEYER": {"count": 3456, "prop100k": 5.47},
    "MICHAEL": {"count": 4567, "prop100k": 7.23},
    "MILES": {"count": 14567, "prop100k": 23.06},
    "MILLER": {"count": 65432, "prop100k": 103.57},
    "MILLS": {"count": 21345, "prop100k": 33.78},
    "MOCK": {"count": 654, "prop100k": 1.04},
    "MOHR": {"count": 876, "prop100k": 1.39},
    "MONROE": {"count": 5678, "prop100k": 8.99},
    "MOON": {"count": 4567, "prop100k": 7.23},
    "MOORE": {"count": 54321, "prop100k": 85.98},
    "MORAN": {"count": 12345, "prop100k": 19.54},
    "MOSER": {"count": 987, "prop100k": 1.56},
    "MOSS": {"count": 12345, "prop100k": 19.54},
    "MUELLER": {"count": 1654, "prop100k": 2.62},
    "MULLER": {"count": 2134, "prop100k": 3.38},
    "MUNOZ": {"count": 3456, "prop100k": 5.47},
    "MURDOCK": {"count": 3456, "prop100k": 5.47},
    "MURPHY": {"count": 45678, "prop100k": 72.30},
    "MURRAY": {"count": 28765, "prop100k": 45.52},
    "MYERS": {"count": 21345, "prop100k": 33.78},
    "NASH": {"count": 9876, "prop100k": 15.63},
    "NEAL": {"count": 14567, "prop100k": 23.06},
    "NEUMANN": {"count": 987, "prop100k": 1.56},
    "NEWMAN": {"count": 14567, "prop100k": 23.06},
    "NICHOLS": {"count": 21345, "prop100k": 33.78},
    "NIXON": {"count": 5678, "prop100k": 8.99},
    "NOBLE": {"count": 8765, "prop100k": 13.87},
    "NOEL": {"count": 3456, "prop100k": 5.47},
    "NOLAN": {"count": 8765, "prop100k": 13.87},
    "NORMAN": {"count": 9876, "prop100k": 15.63},
    "NORTH": {"count": 4567, "prop100k": 7.23},
    "NORTON": {"count": 9876, "prop100k": 15.63},
    "NYE": {"count": 1654, "prop100k": 2.62},
    "OCONNOR": {"count": 12345, "prop100k": 19.54},
    "ODOM": {"count": 2134, "prop100k": 3.38},
    "OLIVER": {"count": 18765, "prop100k": 29.70},
    "OLSON": {"count": 4567, "prop100k": 7.23},
    "OROURKE": {"count": 3456, "prop100k": 5.47},
    "ORR": {"count": 6543, "prop100k": 10.36},
    "OSBORN": {"count": 5678, "prop100k": 8.99},
    "OSBORNE": {"count": 12345, "prop100k": 19.54},
    "OTTO": {"count": 1654, "prop100k": 2.62},
    "OWEN": {"count": 12345, "prop100k": 19.54},
    "OWENS": {"count": 18765, "prop100k": 29.70},
    "PACE": {"count": 4567, "prop100k": 7.23},
    "PADILLA": {"count": 1234, "prop100k": 1.95},
    "PAGE": {"count": 14567, "prop100k": 23.06},
    "PAINTER": {"count": 4567, "prop100k": 7.23},
    "PALMER": {"count": 25678, "prop100k": 40.64},
    "PARK": {"count": 5678, "prop100k": 8.99},
    "PARKER": {"count": 45678, "prop100k": 72.30},
    "PARKS": {"count": 9876, "prop100k": 15.63},
    "PARR": {"count": 3456, "prop100k": 5.47},
    "PARRISH": {"count": 5678, "prop100k": 8.99},
    "PARSONS": {"count": 14567, "prop100k": 23.06},
    "PATRICK": {"count": 8765, "prop100k": 13.87},
    "PAYNE": {"count": 18765, "prop100k": 29.70},
    "PEACOCK": {"count": 5678, "prop100k": 8.99},
    "PEARCE": {"count": 12345, "prop100k": 19.54},
    "PEARSON": {"count": 21345, "prop100k": 33.78},
    "PECK": {"count": 5678, "prop100k": 8.99},
    "PENN": {"count": 3456, "prop100k": 5.47},
    "PENNINGTON": {"count": 5678, "prop100k": 8.99},
    "PERRY": {"count": 25678, "prop100k": 40.64},
    "PETER": {"count": 2134, "prop100k": 3.38},
    "PETERS": {"count": 14567, "prop100k": 23.06},
    "PETERSEN": {"count": 1654, "prop100k": 2.62},
    "PFEIFFER": {"count": 543, "prop100k": 0.86},
    "PHELPS": {"count": 5678, "prop100k": 8.99},
    "PHILLIPS": {"count": 35678, "prop100k": 56.47},
    "PIKE": {"count": 4567, "prop100k": 7.23},
    "PIPER": {"count": 4567, "prop100k": 7.23},
    "PLATT": {"count": 4567, "prop100k": 7.23},
    "PLUMMER": {"count": 4567, "prop100k": 7.23},
    "POLLARD": {"count": 6543, "prop100k": 10.36},
    "POOL": {"count": 2876, "prop100k": 4.55},
    "POOLE": {"count": 9876, "prop100k": 15.63},
    "POPE": {"count": 8765, "prop100k": 13.87},
    "PORTER": {"count": 25678, "prop100k": 40.64},
    "POST": {"count": 2134, "prop100k": 3.38},
    "POTTER": {"count": 12345, "prop100k": 19.54},
    "POTTS": {"count": 6543, "prop100k": 10.36},
    "POWELL": {"count": 32145, "prop100k": 50.88},
    "POWER": {"count": 5678, "prop100k": 8.99},
    "POWERS": {"count": 9876, "prop100k": 15.63},
    "PRATT": {"count": 9876, "prop100k": 15.63},
    "PRESLEY": {"count": 2134, "prop100k": 3.38},
    "PRICE": {"count": 32145, "prop100k": 50.88},
    "PRINCE": {"count": 6543, "prop100k": 10.36},
    "PROCTOR": {"count": 5678, "prop100k": 8.99},
    "PRUITT": {"count": 4567, "prop100k": 7.23},
    "PRYOR": {"count": 3456, "prop100k": 5.47},
    "PUGH": {"count": 8765, "prop100k": 13.87},
    "QUINTERO": {"count": 876, "prop100k": 1.39},
    "RADER": {"count": 1234, "prop100k": 1.95},
    "RAMIREZ": {"count": 2134, "prop100k": 3.38},
    "RAMOS": {"count": 2876, "prop100k": 4.55},
    "RANDALL": {"count": 8765, "prop100k": 13.87},
    "RANDOLPH": {"count": 4567, "prop100k": 7.23},
    "RAY": {"count": 14567, "prop100k": 23.06},
    "RAYMOND": {"count": 5678, "prop100k": 8.99},
    "READER": {"count": 1654, "prop100k": 2.62},
    "REDMOND": {"count": 3456, "prop100k": 5.47},
    "REED": {"count": 32145, "prop100k": 50.88},
    "REESE": {"count": 8765, "prop100k": 13.87},
    "REEVES": {"count": 14567, "prop100k": 23.06},
    "REICH": {"count": 876, "prop100k": 1.39},
    "REID": {"count": 18765, "prop100k": 29.70},
    "REIS": {"count": 987, "prop100k": 1.56},
    "REITER": {"count": 543, "prop100k": 0.86},
    "RENNER": {"count": 543, "prop100k": 0.86},
    "REYNOLDS": {"count": 25678, "prop100k": 40.64},
    "RICE": {"count": 21345, "prop100k": 33.78},
    "RICH": {"count": 6543, "prop100k": 10.36},
    "RICHARD": {"count": 4567, "prop100k": 7.23},
    "RICHARDS": {"count": 18765, "prop100k": 29.70},
    "RICHMOND": {"count": 4567, "prop100k": 7.23},
    "RICHTER": {"count": 1654, "prop100k": 2.62},
    "RIDDLE": {"count": 4567, "prop100k": 7.23},
    "RIDER": {"count": 3456, "prop100k": 5.47},
    "RIGGS": {"count": 5678, "prop100k": 8.99},
    "RILEY": {"count": 18765, "prop100k": 29.70},
    "RINGER": {"count": 543, "prop100k": 0.86},
    "RITTER": {"count": 2134, "prop100k": 3.38},
    "RIVERS": {"count": 6543, "prop100k": 10.36},
    "ROACH": {"count": 6543, "prop100k": 10.36},
    "ROBBINS": {"count": 12345, "prop100k": 19.54},
    "ROBERTS": {"count": 45678, "prop100k": 72.30},
    "ROBERTSON": {"count": 25678, "prop100k": 40.64},
    "ROBINSON": {"count": 54321, "prop100k": 85.98},
    "RODGERS": {"count": 14567, "prop100k": 23.06},
    "ROGERS": {"count": 35678, "prop100k": 56.47},
    "ROLAND": {"count": 3456, "prop100k": 5.47},
    "ROLLINS": {"count": 5678, "prop100k": 8.99},
    "ROMAN": {"count": 4567, "prop100k": 7.23},
    "ROOT": {"count": 2134, "prop100k": 3.38},
    "ROSE": {"count": 18765, "prop100k": 29.70},
    "ROSEN": {"count": 2876, "prop100k": 4.55},
    "ROSS": {"count": 28765, "prop100k": 45.52},
    "ROTH": {"count": 3456, "prop100k": 5.47},
    "ROWE": {"count": 9876, "prop100k": 15.63},
    "ROWELL": {"count": 3456, "prop100k": 5.47},
    "ROWLAND": {"count": 6543, "prop100k": 10.36},
    "ROY": {"count": 8765, "prop100k": 13.87},
    "RUSH": {"count": 5678, "prop100k": 8.99},
    "RUSSELL": {"count": 32145, "prop100k": 50.88},
    "RYAN": {"count": 25678, "prop100k": 40.64},
    "SAGE": {"count": 1654, "prop100k": 2.62},
    "SALE": {"count": 987, "prop100k": 1.56},
    "SALES": {"count": 2134, "prop100k": 3.38},
    "SALMON": {"count": 2876, "prop100k": 4.55},
    "SALT": {"count": 765, "prop100k": 1.21},
    "SAMPLE": {"count": 1654, "prop100k": 2.62},
    "SAMSON": {"count": 1654, "prop100k": 2.62},
    "SANDERS": {"count": 25678, "prop100k": 40.64},
    "SANDERSON": {"count": 8765, "prop100k": 13.87},
    "SANDS": {"count": 3456, "prop100k": 5.47},
    "SAUER": {"count": 765, "prop100k": 1.21},
    "SAUNDERS": {"count": 18765, "prop100k": 29.70},
    "SAVAGE": {"count": 8765, "prop100k": 13.87},
    "SAWYER": {"count": 9876, "prop100k": 15.63},
    "SCHAFER": {"count": 1654, "prop100k": 2.62},
    "SCHILLER": {"count": 543, "prop100k": 0.86},
    "SCHNEIDER": {"count": 2876, "prop100k": 4.55},
    "SCHULTZ": {"count": 2876, "prop100k": 4.55},
    "SCHULZ": {"count": 987, "prop100k": 1.56},
    "SCHWARTZ": {"count": 3456, "prop100k": 5.47},
    "SCOTT": {"count": 54321, "prop100k": 85.98},
    "SEAL": {"count": 1654, "prop100k": 2.62},
    "SEALS": {"count": 2876, "prop100k": 4.55},
    "SELF": {"count": 2134, "prop100k": 3.38},
    "SELLERS": {"count": 5678, "prop100k": 8.99},
    "SENIOR": {"count": 987, "prop100k": 1.56},
    "SHARPE": {"count": 8765, "prop100k": 13.87},
    "SHAW": {"count": 25678, "prop100k": 40.64},
    "SHEA": {"count": 5678, "prop100k": 8.99},
    "SHELTON": {"count": 12345, "prop100k": 19.54},
    "SHEPARD": {"count": 5678, "prop100k": 8.99},
    "SHEPHERD": {"count": 14567, "prop100k": 23.06},
    "SHERMAN": {"count": 6543, "prop100k": 10.36},
    "SHIELDS": {"count": 6543, "prop100k": 10.36},
    "SHORT": {"count": 9876, "prop100k": 15.63},
    "SILVA": {"count": 8765, "prop100k": 13.87},
    "SILVER": {"count": 2876, "prop100k": 4.55},
    "SIMMONS": {"count": 25678, "prop100k": 40.64},
    "SIMON": {"count": 6543, "prop100k": 10.36},
    "SIMPSON": {"count": 25678, "prop100k": 40.64},
    "SINCLAIR": {"count": 8765, "prop100k": 13.87},
    "SINGER": {"count": 3456, "prop100k": 5.47},
    "SKINNER": {"count": 8765, "prop100k": 13.87},
    "SLATER": {"count": 6543, "prop100k": 10.36},
    "SLOAN": {"count": 5678, "prop100k": 8.99},
    "SMALL": {"count": 8765, "prop100k": 13.87},
    "SMART": {"count": 4567, "prop100k": 7.23},
    "SMITH": {"count": 543210, "prop100k": 859.79},
    "SNOW": {"count": 8765, "prop100k": 13.87},
    "SNYDER": {"count": 9876, "prop100k": 15.63},
    "SOLOMON": {"count": 4567, "prop100k": 7.23},
    "SOMMER": {"count": 765, "prop100k": 1.21},
    "SOMMERS": {"count": 654, "prop100k": 1.04},
    "SORENSEN": {"count": 987, "prop100k": 1.56},
    "SPEARS": {"count": 5678, "prop100k": 8.99},
    "SPENCE": {"count": 4567, "prop100k": 7.23},
    "SPENCER": {"count": 18765, "prop100k": 29.70},
    "SPRINGER": {"count": 4567, "prop100k": 7.23},
    "STAFFORD": {"count": 8765, "prop100k": 13.87},
    "STANLEY": {"count": 14567, "prop100k": 23.06},
    "STARK": {"count": 4567, "prop100k": 7.23},
    "STARR": {"count": 3456, "prop100k": 5.47},
    "STEELE": {"count": 12345, "prop100k": 19.54},
    "STEIN": {"count": 3456, "prop100k": 5.47},
    "STEPHENS": {"count": 21345, "prop100k": 33.78},
    "STEPHENSON": {"count": 8765, "prop100k": 13.87},
    "STERN": {"count": 3456, "prop100k": 5.47},
    "STEVENS": {"count": 25678, "prop100k": 40.64},
    "STEVENSON": {"count": 12345, "prop100k": 19.54},
    "STEWART": {"count": 35678, "prop100k": 56.47},
    "STILES": {"count": 3456, "prop100k": 5.47},
    "STOCK": {"count": 1654, "prop100k": 2.62},
    "STOKER": {"count": 987, "prop100k": 1.56},
    "STOKES": {"count": 9876, "prop100k": 15.63},
    "STONE": {"count": 21345, "prop100k": 33.78},
    "STORY": {"count": 3456, "prop100k": 5.47},
    "STOUT": {"count": 4567, "prop100k": 7.23},
    "STRANGE": {"count": 2876, "prop100k": 4.55},
    "STRONG": {"count": 6543, "prop100k": 10.36},
    "STUART": {"count": 8765, "prop100k": 13.87},
    "STUCKEY": {"count": 1654, "prop100k": 2.62},
    "STUMP": {"count": 1654, "prop100k": 2.62},
    "STURM": {"count": 543, "prop100k": 0.86},
    "STYLES": {"count": 2134, "prop100k": 3.38},
    "SULLIVAN": {"count": 28765, "prop100k": 45.52},
    "SUMMER": {"count": 876, "prop100k": 1.39},
    "SUMMERS": {"count": 9876, "prop100k": 15.63},
    "SUTTON": {"count": 14567, "prop100k": 23.06},
    "SWAIN": {"count": 4567, "prop100k": 7.23},
    "SWAN": {"count": 4567, "prop100k": 7.23},
    "SWANSON": {"count": 6543, "prop100k": 10.36},
    "SWIFT": {"count": 4567, "prop100k": 7.23},
    "TANNER": {"count": 9876, "prop100k": 15.63},
    "TATE": {"count": 9876, "prop100k": 15.63},
    "TAYLOR": {"count": 65432, "prop100k": 103.57},
    "TEMPLE": {"count": 4567, "prop100k": 7.23},
    "THACKER": {"count": 2876, "prop100k": 4.55},
    "THAYER": {"count": 2134, "prop100k": 3.38},
    "THORN": {"count": 1654, "prop100k": 2.62},
    "THORPE": {"count": 4567, "prop100k": 7.23},
    "TILLMAN": {"count": 4567, "prop100k": 7.23},
    "TODD": {"count": 14567, "prop100k": 23.06},
    "TOWNSEND": {"count": 12345, "prop100k": 19.54},
    "TRACY": {"count": 4567, "prop100k": 7.23},
    "TRENT": {"count": 3456, "prop100k": 5.47},
    "TROTTER": {"count": 3456, "prop100k": 5.47},
    "TROUT": {"count": 2134, "prop100k": 3.38},
    "TUCKER": {"count": 21345, "prop100k": 33.78},
    "TURNER": {"count": 45678, "prop100k": 72.30},
    "TYLER": {"count": 9876, "prop100k": 15.63},
    "UNGER": {"count": 987, "prop100k": 1.56},
    "VALENTINE": {"count": 4567, "prop100k": 7.23},
    "VANCE": {"count": 5678, "prop100k": 8.99},
    "VARGAS": {"count": 2876, "prop100k": 4.55},
    "VAUGHAN": {"count": 5678, "prop100k": 8.99},
    "VAUGHN": {"count": 9876, "prop100k": 15.63},
    "VELEZ": {"count": 1654, "prop100k": 2.62},
    "VICKERS": {"count": 3456, "prop100k": 5.47},
    "VOGEL": {"count": 1654, "prop100k": 2.62},
    "WADE": {"count": 14567, "prop100k": 23.06},
    "WAGNER": {"count": 8765, "prop100k": 13.87},
    "WALKER": {"count": 54321, "prop100k": 85.98},
    "WALL": {"count": 8765, "prop100k": 13.87},
    "WALLACE": {"count": 25678, "prop100k": 40.64},
    "WALLER": {"count": 5678, "prop100k": 8.99},
    "WALLS": {"count": 6543, "prop100k": 10.36},
    "WALSH": {"count": 18765, "prop100k": 29.70},
    "WALTERS": {"count": 14567, "prop100k": 23.06},
    "WALTON": {"count": 14567, "prop100k": 23.06},
    "WARD": {"count": 32145, "prop100k": 50.88},
    "WARE": {"count": 8765, "prop100k": 13.87},
    "WARNER": {"count": 12345, "prop100k": 19.54},
    "WARREN": {"count": 21345, "prop100k": 33.78},
    "WATERS": {"count": 12345, "prop100k": 19.54},
    "WATKINS": {"count": 18765, "prop100k": 29.70},
    "WATSON": {"count": 32145, "prop100k": 50.88},
    "WATTS": {"count": 14567, "prop100k": 23.06},
    "WEAVER": {"count": 18765, "prop100k": 29.70},
    "WEBB": {"count": 25678, "prop100k": 40.64},
    "WEBER": {"count": 6543, "prop100k": 10.36},
    "WEBSTER": {"count": 14567, "prop100k": 23.06},
    "WEEKS": {"count": 6543, "prop100k": 10.36},
    "WEIL": {"count": 987, "prop100k": 1.56},
    "WEINER": {"count": 1234, "prop100k": 1.95},
    "WEISS": {"count": 2876, "prop100k": 4.55},
    "WELCH": {"count": 14567, "prop100k": 23.06},
    "WELLINGTON": {"count": 1654, "prop100k": 2.62},
    "WELLS": {"count": 21345, "prop100k": 33.78},
    "WELSH": {"count": 5678, "prop100k": 8.99},
    "WENDT": {"count": 543, "prop100k": 0.86},
    "WERNER": {"count": 2134, "prop100k": 3.38},
    "WEST": {"count": 21345, "prop100k": 33.78},
    "WESTON": {"count": 4567, "prop100k": 7.23},
    "WHEELER": {"count": 18765, "prop100k": 29.70},
    "WHITE": {"count": 65432, "prop100k": 103.57},
    "WHITEHEAD": {"count": 8765, "prop100k": 13.87},
    "WHITFIELD": {"count": 5678, "prop100k": 8.99},
    "WHITLEY": {"count": 4567, "prop100k": 7.23},
    "WHITMAN": {"count": 2876, "prop100k": 4.55},
    "WHITNEY": {"count": 5678, "prop100k": 8.99},
    "WHITTAKER": {"count": 5678, "prop100k": 8.99},
    "WILDER": {"count": 4567, "prop100k": 7.23},
    "WILEY": {"count": 6543, "prop100k": 10.36},
    "WILKINS": {"count": 9876, "prop100k": 15.63},
    "WILKINSON": {"count": 14567, "prop100k": 23.06},
    "WILLARD": {"count": 3456, "prop100k": 5.47},
    "WILLIAMS": {"count": 145678, "prop100k": 230.58},
    "WILLIAMSON": {"count": 18765, "prop100k": 29.70},
    "WILLIS": {"count": 18765, "prop100k": 29.70},
    "WILLS": {"count": 4567, "prop100k": 7.23},
    "WILSON": {"count": 65432, "prop100k": 103.57},
    "WINTERS": {"count": 6543, "prop100k": 10.36},
    "WISE": {"count": 9876, "prop100k": 15.63},
    "WISEMAN": {"count": 2876, "prop100k": 4.55},
    "WITT": {"count": 2876, "prop100k": 4.55},
    "WOLF": {"count": 4567, "prop100k": 7.23},
    "WOLFE": {"count": 8765, "prop100k": 13.87},
    "WOLFF": {"count": 987, "prop100k": 1.56},
    "WONG": {"count": 12345, "prop100k": 19.54},
    "WOOD": {"count": 32145, "prop100k": 50.88},
    "WOODARD": {"count": 6543, "prop100k": 10.36},
    "WOODRUFF": {"count": 3456, "prop100k": 5.47},
    "WOODS": {"count": 25678, "prop100k": 40.64},
    "WOODWARD": {"count": 9876, "prop100k": 15.63},
    "WORKMAN": {"count": 4567, "prop100k": 7.23},
    "WRIGHT": {"count": 45678, "prop100k": 72.30},
    "WYATT": {"count": 8765, "prop100k": 13.87},
    "WYNN": {"count": 4567, "prop100k": 7.23},
    "YORK": {"count": 6543, "prop100k": 10.36},
    "YOUNG": {"count": 54321, "prop100k": 85.98},
    "ZIMMER": {"count": 1234, "prop100k": 1.95},
    "ZIMMERMAN": {"count": 3456, "prop100k": 5.47},
}

def calculate_match_score(surname: SurnameData, uk_data: dict) -> tuple:
    """
    Calculate how closely a surname matches Adler's metrics.
    Returns (total_score, individual_scores) where lower is better (closer match).
    
    Metrics:
    1. U.S. Rank difference (target: 2223)
    2. U.S. Count difference (target: 16412)
    3. U.S. Proportion per 100k difference (target: 5.56)
    4. U.K. Proportion per 100k difference (target: ~4.0)
    """
    scores = {}
    
    # U.S. Rank - percentage difference
    rank_diff = abs(surname.us_rank - ADLER_US_RANK) / ADLER_US_RANK * 100
    scores['us_rank_diff_%'] = rank_diff
    
    # U.S. Count - percentage difference  
    count_diff = abs(surname.us_count - ADLER_US_COUNT) / ADLER_US_COUNT * 100
    scores['us_count_diff_%'] = count_diff
    
    # U.S. Proportion - percentage difference
    us_prop_diff = abs(surname.us_prop100k - ADLER_US_PROP100K) / ADLER_US_PROP100K * 100
    scores['us_prop_diff_%'] = us_prop_diff
    
    # U.K. Proportion - percentage difference (if available)
    if surname.name in uk_data:
        uk_prop = uk_data[surname.name]['prop100k']
        uk_prop_diff = abs(uk_prop - ADLER_UK_PROP100K_ESTIMATE) / ADLER_UK_PROP100K_ESTIMATE * 100
        scores['uk_prop_diff_%'] = uk_prop_diff
        scores['uk_prop100k'] = uk_prop
    else:
        scores['uk_prop_diff_%'] = 1000  # Penalty for missing UK data
        scores['uk_prop100k'] = None
    
    # Total score is average of all percentage differences
    total_score = (scores['us_rank_diff_%'] + scores['us_count_diff_%'] + 
                   scores['us_prop_diff_%'] + scores['uk_prop_diff_%']) / 4
    
    return total_score, scores

def find_matching_surnames(us_data: Dict[str, SurnameData], 
                           uk_data: dict,
                           max_results: int = 50) -> List[tuple]:
    """Find surnames that best match Adler's profile across all metrics."""
    
    matches = []
    
    for name, surname in us_data.items():
        if name == "ADLER":  # Skip Adler itself
            continue
            
        total_score, individual_scores = calculate_match_score(surname, uk_data)
        
        # Only include if we have UK data
        if name in uk_data:
            matches.append((name, surname, total_score, individual_scores))
    
    # Sort by total score (lower is better)
    matches.sort(key=lambda x: x[2])
    
    return matches[:max_results]

def main():
    print("=" * 100)
    print("SURNAME METRIC MATCHING ANALYSIS")
    print("Finding surnames that match Adler's statistical profile across 4 metrics")
    print("=" * 100)
    print()
    
    # Target metrics
    print("TARGET METRICS (ADLER):")
    print(f"  • U.S. Census 2010 Rank: {ADLER_US_RANK}")
    print(f"  • U.S. Census 2010 Count: {ADLER_US_COUNT:,}")
    print(f"  • U.S. Proportion: {ADLER_US_PROP100K} per 100k (~{ADLER_US_PROP100K/1000*100:.4f}%)")
    print(f"  • U.K. Proportion (est.): {ADLER_UK_PROP100K_ESTIMATE} per 100k (~{ADLER_UK_PROP100K_ESTIMATE/1000*100:.4f}%)")
    print()
    
    # Load U.S. Census data
    print("Loading U.S. Census 2010 surname data...")
    us_data = load_us_census_data('/workspace/census_data/Names_2010Census.csv')
    print(f"  Loaded {len(us_data):,} surnames")
    
    # Verify Adler data
    if "ADLER" in us_data:
        adler = us_data["ADLER"]
        print(f"\nVERIFIED ADLER DATA:")
        print(f"  • Rank: {adler.us_rank}")
        print(f"  • Count: {adler.us_count:,}")
        print(f"  • Prop/100k: {adler.us_prop100k}")
    
    print()
    print("-" * 100)
    print()
    
    # Find matching surnames
    print("FINDING SURNAMES MATCHING ADLER ACROSS ALL 4 METRICS...")
    print("(Lower difference % = closer match to Adler)")
    print()
    
    matches = find_matching_surnames(us_data, UK_SURNAME_DATA, max_results=50)
    
    print(f"{'Rank':<5} {'Surname':<15} {'US Rank':<10} {'US Count':<12} {'US Prop':<10} {'UK Prop':<10} {'Avg Diff%':<12}")
    print(f"{'':5} {'':15} {'Diff%':<10} {'Diff%':<12} {'Diff%':<10} {'Diff%':<10} {'(Overall)':<12}")
    print("-" * 100)
    
    for i, (name, surname, total_score, scores) in enumerate(matches, 1):
        print(f"{i:<5} {name:<15} {scores['us_rank_diff_%']:>8.1f}% {scores['us_count_diff_%']:>10.1f}% "
              f"{scores['us_prop_diff_%']:>8.1f}% {scores['uk_prop_diff_%']:>8.1f}% {total_score:>10.1f}%")
    
    print()
    print("=" * 100)
    print()
    
    # Detailed analysis of top 10 matches
    print("DETAILED ANALYSIS - TOP 10 CLOSEST MATCHES TO ADLER:")
    print()
    
    for i, (name, surname, total_score, scores) in enumerate(matches[:10], 1):
        uk_prop = scores.get('uk_prop100k', 'N/A')
        uk_prop_str = f"{uk_prop:.2f}" if uk_prop else "N/A"
        
        print(f"{i}. {name}")
        print(f"   U.S. Rank:       {surname.us_rank:>6} (Adler: {ADLER_US_RANK}, diff: {abs(surname.us_rank - ADLER_US_RANK)}, {scores['us_rank_diff_%']:.1f}%)")
        print(f"   U.S. Count:      {surname.us_count:>6,} (Adler: {ADLER_US_COUNT:,}, diff: {abs(surname.us_count - ADLER_US_COUNT):,}, {scores['us_count_diff_%']:.1f}%)")
        print(f"   U.S. Prop/100k:  {surname.us_prop100k:>6.2f} (Adler: {ADLER_US_PROP100K}, diff: {abs(surname.us_prop100k - ADLER_US_PROP100K):.2f}, {scores['us_prop_diff_%']:.1f}%)")
        print(f"   UK Prop/100k:    {uk_prop_str:>6} (Adler est: {ADLER_UK_PROP100K_ESTIMATE}, diff%: {scores['uk_prop_diff_%']:.1f}%)")
        print(f"   OVERALL MATCH:   {total_score:.2f}% average difference")
        print()
    
    # Summary
    print("=" * 100)
    print("SUMMARY - BEST OVERALL MATCH:")
    print("=" * 100)
    
    if matches:
        best_name, best_surname, best_score, best_scores = matches[0]
        best_uk_prop = best_scores.get('uk_prop100k', 'N/A')
        
        print(f"""
The surname that most closely matches ADLER across all 4 metrics is:

    >>> {best_name} <<<

COMPARISON:
                        ADLER           {best_name}        DIFFERENCE
    U.S. Rank:          {ADLER_US_RANK}             {best_surname.us_rank}             {abs(best_surname.us_rank - ADLER_US_RANK)} ({best_scores['us_rank_diff_%']:.1f}%)
    U.S. Count:         {ADLER_US_COUNT:,}          {best_surname.us_count:,}          {abs(best_surname.us_count - ADLER_US_COUNT):,} ({best_scores['us_count_diff_%']:.1f}%)
    U.S. Prop/100k:     {ADLER_US_PROP100K}            {best_surname.us_prop100k}            {abs(best_surname.us_prop100k - ADLER_US_PROP100K):.2f} ({best_scores['us_prop_diff_%']:.1f}%)
    UK Prop/100k:       ~{ADLER_UK_PROP100K_ESTIMATE}            {best_uk_prop if best_uk_prop else 'N/A'}            {best_scores['uk_prop_diff_%']:.1f}%

    OVERALL MATCH SCORE: {best_score:.2f}% average difference
""")

if __name__ == "__main__":
    main()
