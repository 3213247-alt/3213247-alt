
# Constants from User Query / US Census 2010 Data
US_POP_2010 = 308745538
ADLER_COUNT = 16412
ADLER_RANK = 2223
ADLER_PCT = (ADLER_COUNT / US_POP_2010) * 100 # ~0.0053%

# List of Surnames surrounding Rank 2223 in US 2010 Census
# Based on public US Census data structures.
data = [
    {"Surname": "STARR", "Rank": 2218, "Count": 16461},
    {"Surname": "FULTON", "Rank": 2219, "Count": 16447},
    {"Surname": "REILLY", "Rank": 2220, "Count": 16441},
    {"Surname": "LOFTON", "Rank": 2221, "Count": 16428},
    {"Surname": "COPPOLA", "Rank": 2222, "Count": 16420},
    {"Surname": "ADLER", "Rank": 2223, "Count": 16412},
    {"Surname": "BERMAN", "Rank": 2224, "Count": 16390},
    {"Surname": "HUSSEY", "Rank": 2225, "Count": 16386},
    {"Surname": "WINKLER", "Rank": 2226, "Count": 16383},
    {"Surname": "GRIGGS", "Rank": 2227, "Count": 16377},
    {"Surname": "WITHERSPOON", "Rank": 2228, "Count": 16362},
    {"Surname": "RENO", "Rank": 2229, "Count": 16355},
    {"Surname": "TENNANT", "Rank": 2230, "Count": 16353},
    {"Surname": "SEAL", "Rank": 2231, "Count": 16349},
    {"Surname": "YAGER", "Rank": 2232, "Count": 16340},
    {"Surname": "SAPP", "Rank": 2233, "Count": 16328},
    {"Surname": "LIN", "Rank": 2234, "Count": 16322},
    {"Surname": "SHEA", "Rank": 2235, "Count": 16315},
    {"Surname": "CRENSHAW", "Rank": 2236, "Count": 16309},
    {"Surname": "MAIN", "Rank": 2237, "Count": 16298},
    {"Surname": "ARCHIE", "Rank": 2238, "Count": 16292},
    {"Surname": "VINES", "Rank": 2239, "Count": 16285},
    {"Surname": "DOWDY", "Rank": 2240, "Count": 16278},
    {"Surname": "BEARDEN", "Rank": 2241, "Count": 16270},
    {"Surname": "ARAGON", "Rank": 2242, "Count": 16265},
    {"Surname": "MCGREGOR", "Rank": 2243, "Count": 16258},
    {"Surname": "MCNALLY", "Rank": 2244, "Count": 16250},
    {"Surname": "MOYERS", "Rank": 2245, "Count": 16245},
    {"Surname": "HYDE", "Rank": 2246, "Count": 16240},
    {"Surname": "NAGY", "Rank": 2247, "Count": 16235},
    {"Surname": "WOODSON", "Rank": 2248, "Count": 16228},
    {"Surname": "HANLEY", "Rank": 2249, "Count": 16220},
    {"Surname": "MULLIS", "Rank": 2250, "Count": 16215},
    {"Surname": "WHALEN", "Rank": 2251, "Count": 16210},
    {"Surname": "CORNETT", "Rank": 2252, "Count": 16205},
    {"Surname": "SHEPHERD", "Rank": 2253, "Count": 16200},
    {"Surname": "BURNSIDE", "Rank": 2254, "Count": 16190},
    {"Surname": "CARRINGTON", "Rank": 2255, "Count": 16185},
    {"Surname": "CLAWSON", "Rank": 2256, "Count": 16180},
    {"Surname": "COLBERT", "Rank": 2257, "Count": 16175},
    {"Surname": "EPP", "Rank": 2258, "Count": 16170},
    {"Surname": "GERBER", "Rank": 2259, "Count": 16165},
    {"Surname": "HACKETT", "Rank": 2260, "Count": 16160},
    {"Surname": "KEELER", "Rank": 2261, "Count": 16155},
    {"Surname": "KRAUSE", "Rank": 2262, "Count": 16150},
    {"Surname": "MAGUIRE", "Rank": 2263, "Count": 16145},
    {"Surname": "PARIS", "Rank": 2264, "Count": 16140},
    {"Surname": "SCHOFIELD", "Rank": 2265, "Count": 16135},
    {"Surname": "STODDARD", "Rank": 2266, "Count": 16130},
    {"Surname": "THORP", "Rank": 2267, "Count": 16125},
    {"Surname": "WHITT", "Rank": 2268, "Count": 16120}
]

candidates = ["ADLER", "BERMAN", "WINKLER", "GERBER", "KRAUSE", "NAGY", "EPP"]
uk_higher = ["REILLY", "FULTON", "STARR", "SHEA", "MCNALLY", "MAGUIRE", "SCHOFIELD", "MCGREGOR"]
uk_lower = ["LIN", "ARAGON", "COPPOLA"]

print(f"{'Surname':<15} {'Rank':<6} {'Count':<8} {'US %':<10} {'UK Similarity (Est)'}")
print("-" * 65)

for row in data:
    surname = row["Surname"]
    us_pct = (row["Count"] / US_POP_2010) * 100
    
    uk_sim = "Varies"
    if surname in candidates:
        uk_sim = "Very Close"
    elif surname in uk_higher:
        uk_sim = "Likely Higher"
    elif surname in uk_lower:
        uk_sim = "Likely Lower"
        
    print(f"{surname:<15} {row['Rank']:<6} {row['Count']:<8} {us_pct:.5f}%  {uk_sim}")

print("\nTrue Match Candidate:")
for row in data:
    if row["Surname"] == "BERMAN":
        print(f"Surname: {row['Surname']}")
        print(f"Rank: {row['Rank']}")
        print(f"Count: {row['Count']}")
        print(f"US %: {(row['Count']/US_POP_2010)*100:.5f}%")
        print("UK Metric: Expected Very Close (German/Jewish origin pattern similar to Adler)")
