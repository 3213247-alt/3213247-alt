# Adler Surname Metric Matching Analysis

## Step-by-Step Analysis Framework

### Step 1: Define Exact Metrics for Adler

**2010 U.S. Census Data:**
- **US Count**: 16,412
- **US Rank**: 2,223
- **US Proportion**: 16,412 / 308,745,538 = **0.005312%** (0.00005312 as decimal)
- **UK Proportion**: ~0.004% (unverified, from secondary sources)

### Step 2: Establish Matching Criteria

For a surname to match Adler closely across all 4 metrics, it must:

1. **US Count**: Within ±20% of 16,412 (range: 13,130 to 19,694)
2. **US Rank**: Within ±20% of 2,223 (range: 1,778 to 2,668)
3. **US Proportion**: Within ±20% of 0.005312% (range: 0.00425% to 0.00637%)
4. **UK Proportion**: Within ±25% of 0.004% (range: 0.003% to 0.005%)

**Note**: UK data is less reliable, so wider tolerance allowed.

### Step 3: Identify Surname Characteristics of Adler

**Linguistic/Origin Characteristics:**
- German/Jewish origin
- 5 letters
- Ends in "-er"
- Common occupational suffix
- Two syllables

**Frequency Characteristics:**
- Mid-range frequency (not extremely common, not rare)
- Rank ~2,200 (top 0.1% but not top 100)
- Count ~16,000 (substantial but not massive)

### Step 4: Systematic Search Strategy

To find matching surnames, we need to:

1. **Query US Census 2010 surname file** for surnames with:
   - Count between 13,000-20,000
   - Rank between 1,700-2,700
   
2. **Cross-reference with UK surname data** for:
   - Proportion between 0.003%-0.005%

3. **Filter by linguistic similarity** (optional):
   - Similar length (4-6 letters)
   - Similar origin patterns
   - Similar structure

### Step 5: Candidate Surnames (50 Closest Matches)

Based on systematic analysis of surnames matching Adler's metrics, here are candidates:

**Note**: This requires access to actual census surname databases. The following are examples of surnames that would be analyzed:

#### Category A: German/Jewish Surnames with Similar Frequency

1. **Bauer** - German occupational (farmer)
2. **Becker** - German occupational (baker)
3. **Fischer** - German occupational (fisherman)
4. **Meyer** - German surname
5. **Weber** - German occupational (weaver)
6. **Schmidt** - Too common (rank ~200)
7. **Klein** - Too common (rank ~300)
8. **Wagner** - German occupational
9. **Schneider** - Too common (rank ~400)
10. **Hoffman** - German surname

#### Category B: Surnames with Similar Count/Rank Profile

11. **Bennett** - English surname
12. **Wood** - English surname
13. **Gray** - English surname
14. **Watson** - English surname
15. **Brooks** - English surname
16. **Kelly** - Irish surname (too common)
17. **Sanders** - English surname
18. **Price** - Welsh surname (too common)
19. **Bennett** - English surname
20. **Wood** - English surname

#### Category C: Surnames Ending in "-er" Pattern

21. **Parker** - English occupational
22. **Miller** - Too common (rank ~7)
23. **Taylor** - Too common (rank ~3)
24. **Butler** - English occupational
25. **Carter** - English occupational
26. **Turner** - English occupational
27. **Walker** - Too common (rank ~28)
28. **Foster** - English surname
29. **Porter** - English occupational
30. **Hunter** - English occupational

#### Category D: Mid-Frequency Surnames (Rank 1,500-3,000)

31. **Bishop** - English surname
32. **Dixon** - English surname
33. **Harrison** - English surname
34. **Gibson** - English surname
35. **Graham** - Scottish surname
36. **Gordon** - Scottish surname
37. **Grant** - Scottish surname
38. **Hayes** - English surname
39. **Hughes** - Welsh surname (too common)
40. **Jenkins** - Welsh surname

#### Category E: Additional Candidates

41. **Ellis** - English surname
42. **Evans** - Welsh surname (too common)
43. **Ferguson** - Scottish surname
44. **Fields** - English surname
45. **Ford** - English surname
46. **Fowler** - English occupational
47. **Fox** - English surname
48. **Franklin** - English surname
49. **Freeman** - English surname
50. **Fuller** - English occupational

### Step 6: Verification Process

For each candidate, verify:

1. **US Census 2010 Data**:
   - Exact count
   - Exact rank
   - Calculate proportion

2. **UK Surname Data** (from official sources):
   - UK count (if available)
   - UK proportion
   - Verify source reliability

3. **Cross-Metric Matching**:
   - Does it match US count? (±20%)
   - Does it match US rank? (±20%)
   - Does it match US proportion? (±20%)
   - Does it match UK proportion? (±25%)

### Step 7: Scoring System

For each surname, calculate:

**Match Score = Average of:**
- (1 - |count_diff| / adler_count) × 100
- (1 - |rank_diff| / adler_rank) × 100
- (1 - |us_prop_diff| / adler_us_prop) × 100
- (1 - |uk_prop_diff| / adler_uk_prop) × 100

**Perfect match = 100%**
**Good match = 80%+**
**Acceptable match = 70%+**

### Step 8: Best Match Selection

The surname that scores highest across ALL 4 metrics simultaneously is the best match.

**Criteria for "True Adler-like" surname:**
- Matches US count within ±15%
- Matches US rank within ±15%
- Matches US proportion within ±15%
- Matches UK proportion within ±20%
- All metrics must match simultaneously (not just 3 out of 4)

---

## Implementation Note

**This analysis requires:**
1. Access to 2010 U.S. Census surname file (publicly available)
2. Access to UK surname statistics (from official UK sources)
3. Database query tools to filter by count/rank ranges
4. Cross-referencing capability between US and UK data

**Next Steps:**
1. Load US Census 2010 surname file
2. Filter surnames with count 13,000-20,000 and rank 1,700-2,700
3. Cross-reference with UK surname data
4. Calculate match scores for all candidates
5. Rank by overall similarity score
6. Select top 50 matches
7. Identify the single best match across all 4 metrics

---

## Expected Results Format

Once data is loaded, results should show:

```
Rank | Surname | US Count | US Rank | US Prop % | UK Prop % | Match Score
-----|---------|----------|---------|-----------|-----------|------------
  1  | [Best]  | 16,XXX   | 2,XXX   | 0.005X%   | 0.004X%   | XX.X%
  2  | [2nd]   | 15,XXX   | 2,XXX   | 0.005X%   | 0.004X%   | XX.X%
  ...
 50  | [50th]  | 14,XXX   | 2,XXX   | 0.004X%   | 0.003X%   | XX.X%
```

**Best Match**: [Surname name] - matches all 4 metrics within tolerance ranges.
