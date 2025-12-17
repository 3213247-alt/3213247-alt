# Actuarial Job Market Analysis: Fact-Checking and Verification

## Purpose
Verify the mathematical calculations and claims about actuarial job market prospects, specifically for candidates starting in 2025 with the profile: 3-4 exams + technical skills (Python/R/SQL) + communication skills.

---

## CLAIM 1: Starting Pool Size - 12,855 Take Exam P

### User's Claim:
"Starting pool (2025): 12,855 take Exam P"

### Verification Status: **CHECKING**

### Actual Data Needed:
- SOA/CAS exam registration numbers
- Historical trends in Exam P registrations

### Search Required:
Need to find actual SOA statistics on annual Exam P sittings.

---

## CLAIM 2: Pass Rate Calculations

### User's Claims:
- Exam P pass rate: ~48%
- Exam FM pass rate: 45-50%
- Exam 3 (FAM/MAS-I) pass rate: ~45%
- Exam 4 pass rate: 40-45%

### Verification Status: **CHECKING**

### Known Data from Industry:
- SOA publishes official pass rates
- Pass rates vary by sitting
- Need to verify specific percentages

---

## CLAIM 3: Attrition Rates in the Funnel

### User's Calculation:
```
Starting: 12,855 take Exam P
After P (48% pass): 6,170
After FM (60% continue, 48% pass): 1,777
After Exam 3 (70% continue, 45% pass): 560
After Exam 4 (60% continue, 42% pass): 141
```

### Issues to Verify:
1. **Attrition assumptions** - Are 60-70% continuation rates accurate?
2. **Compounding effect** - Does the calculation properly account for cumulative attrition?
3. **Time frame** - Are these annual figures or cohort-based?

### Mathematical Check:
- 12,855 × 0.48 = 6,170 ✓ (correct if pass rate is 48%)
- 6,170 × 0.60 × 0.48 = 1,777 ✓ (mathematically correct)
- 1,777 × 0.70 × 0.45 = 560 ✓ (mathematically correct)
- 560 × 0.60 × 0.42 = 141 ✓ (mathematically correct)

**Math is internally consistent, but attrition assumptions need verification.**

---

## CLAIM 4: Technical + Communication Skills Overlay

### User's Calculation:
```
141 people with 4 exams
× 70% have technical skills = 99
× 80% have good communication = 79
Final: ~80-100 people with full profile
```

### Issues:
1. **Sequential vs. Independent probability** - The calculation treats these as sequential (conditional), but they may be independent
2. **Correct calculation if independent**: 141 × 0.70 × 0.80 = 79 people
3. **User's range (80-100)** includes some with 3 exams, which is reasonable

### Verification Status: **MATHEMATICALLY CORRECT** (assuming independence)

### Critical Assumption to Verify:
- What percentage of exam-passers actually have Python/R/SQL skills?
- What percentage have strong communication skills?
- Are these percentages accurate?

---

## CLAIM 5: Total Job Openings - 2,400 Per Year

### User's Claim:
"About 2,400 openings for actuaries are projected each year, on average, over the decade according to the Bureau of Labor Statistics."

### Verification Status: **NEEDS BLS DATA CHECK**

### Known Context:
- BLS projects employment for actuaries
- 2,400 includes ALL openings (entry-level, mid-career, senior, replacements)
- Need to verify actual BLS number

---

## CLAIM 6: Entry-Level Percentage (30-40%)

### User's Calculation:
"If ~2,400 total openings per year, and roughly 30-40% are entry-level (typical for most professions): ~720-960 entry-level positions per year"

### Issues to Verify:
1. **Is 30-40% accurate for actuarial field?**
   - Actuarial field has aging workforce
   - Heavy automation of entry-level work
   - May be lower than 30-40%

2. **Job posting data cited:**
   - Indeed: 294 entry-level jobs (snapshot)
   - Glassdoor: 295-1,435 (snapshot)
   - LinkedIn: 616 (snapshot)

3. **Snapshot vs. Annual:**
   - Job postings stay live 30-60 days typically
   - If 616 on LinkedIn at one time, annual might be: 616 × (365/45) = ~5,000
   - But this includes duplicates, repostings, multiple sites

### Critical Question:
**Is 1,000 entry-level actuarial jobs per year accurate?**

This is the weakest link in the analysis. Need to verify this number.

---

## CLAIM 7: Supply vs. Demand Ratio in 2032

### User's Calculation:
```
Supply: 148-185 fully qualified candidates (from 23,800 starting Exam P)
Demand: 1,157 entry-level jobs (with 2.1% annual growth)
Ratio: 148-185 ÷ 1,157 = 12-16% of jobs filled by fully qualified candidates
```

### Mathematical Verification:
- 2032 is 7 years from 2025
- 1,000 × (1.021)^7 = 1,000 × 1.1572 = 1,157 ✓ (correct)

### Issues:
1. **Where does 8% exam growth come from?**
   - 12,855 → 23,800 is 85% growth, not 8% annual
   - 8% annual for 7 years: 12,855 × (1.08)^7 = 22,026
   - Close to 23,800, so this checks out ✓

2. **Where does 2.1% job growth come from?**
   - Need BLS projection data
   - Is this specific to actuaries or general employment growth?

### Verification Status: **MATH CORRECT, BUT ASSUMPTIONS NEED VERIFICATION**

---

## CLAIM 8: Age Discrimination and Success Rates

### User's Claims:
- 22-year-old with 3-4 exams + tech + communication: **70-80% chance** of getting job by 2032
- 30-year-old starting 4-year degree, graduating at 34: **20-30% chance** of getting job by 2034

### Verification Status: **SUBJECTIVE ESTIMATES**

### Issues:
- No data source provided for these percentages
- Based on anecdotal evidence?
- Industry reports on age discrimination?

### Need to Find:
1. Data on entry-level actuary hiring by age
2. Success rates for career changers
3. Internship requirements and age restrictions

---

## KEY QUESTIONS TO RESEARCH

### Priority 1 (Critical to Analysis):
1. **Actual number of entry-level actuarial jobs per year in U.S.**
   - Is it 500? 1,000? 2,000?
   - This determines if supply/demand analysis is valid

2. **Actual SOA/CAS exam registration numbers**
   - Is 12,855 taking Exam P accurate for 2024-2025?
   - What's the historical trend?

3. **BLS employment projections for actuaries**
   - Total openings per year
   - Growth rate 2025-2032

### Priority 2 (Important for Accuracy):
4. **Actual pass rates by exam**
   - SOA publishes these - need current data

5. **Attrition rates between exams**
   - What percentage continue after passing each exam?
   - Industry data or surveys?

6. **Percentage of exam-passers with technical skills**
   - How many actuarial candidates know Python/R/SQL?
   - Is 70% realistic or optimistic?

### Priority 3 (Contextual):
7. **Age distribution of entry-level hires**
   - Industry surveys on hiring practices
   - Age discrimination data

8. **Internship requirements**
   - What percentage of entry-level hires had internships?
   - Is 85% accurate?

---

## PRELIMINARY ASSESSMENT (Before Research)

### What Appears Accurate:
1. **Mathematical calculations are internally consistent**
   - The funnel math checks out
   - Compound probability calculations correct

2. **General narrative is plausible**
   - Actuarial field is competitive
   - Entry-level is getting harder
   - Age matters for hiring

### What Needs Verification:
1. **Starting numbers** (12,855 taking Exam P)
2. **Entry-level job count** (1,000 per year)
3. **Attrition rates** (60-70% continuing)
4. **Technical skill penetration** (70% with Python/R/SQL)
5. **Growth rates** (8% exam, 2.1% jobs)

### What Appears Questionable:
1. **1,000 entry-level jobs seems HIGH**
   - Job posting snapshots suggest lower number
   - Need to reconcile snapshot data with annual estimates

2. **70% having technical skills seems OPTIMISTIC**
   - Many actuarial candidates still Excel/VBA focused
   - Python/R adoption is growing but may not be 70% yet

3. **Success rate percentages are unsupported**
   - 70-80% for ideal candidate
   - 20-30% for 34-year-old
   - These need data backing

---

## NEXT STEPS

1. Search for SOA/CAS statistical reports
2. Check BLS Occupational Outlook Handbook for actuaries
3. Search for actuarial job market surveys
4. Look for age-related hiring data
5. Calculate more realistic estimates based on actual data
