#!/usr/bin/env python3
"""
Attempt to find U.K. surname data for the top matches.
"""

import csv
import json

# Top matches from U.S. analysis
top_matches = [
    'CHADWICK', 'BARNEY', 'WHITING', 'ENNIS', 'FOOTE', 'ONTIVEROS', 'RING',
    'HUSTON', 'ALTMAN', 'RIDER', 'ABERNATHY', 'JOINER', 'RINCON', 'GOLDSMITH',
    'HOGUE', 'OROURKE', 'EASLEY', 'BAUM', 'PERDUE', 'TAMAYO', 'RUFFIN',
    'LAUGHLIN', 'RADER', 'LINCOLN', 'ANGUIANO', 'BARON', 'TRIMBLE', 'REAGAN',
    'HARE', 'ARNETT', 'RUSS', 'AHMAD', 'ADAMSON', 'PARR', 'BURKHART',
    'MONTANEZ', 'CARRERA', 'AARON', 'DUFF', 'CLINTON', 'WOODALL', 'MALLOY',
    'SCHILLING', 'MARCUM', 'HENNING', 'PAPPAS', 'DOWLING', 'GIORDANO',
    'BALDERAS', 'PICKENS'
]

print("Top 50 U.S. matches that need U.K. data:")
for i, name in enumerate(top_matches, 1):
    print(f"{i:2d}. {name}")

print("\nNote: U.K. surname data would need to be obtained from:")
print("  - Office for National Statistics (ONS) U.K.")
print("  - Forebears.io (requires verification)")
print("  - Other U.K. surname databases")
print("\nFor now, matching is based on 3 U.S. metrics.")
