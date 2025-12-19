import pandas as pd

# Load the CSV
df = pd.read_csv('Names_2010Census.csv')

# Clean headers if needed (usually name,rank,count,prop100k,...)
# The first row might be headers.
# Let's inspect columns first
print("Columns:", df.columns)

# Standardize name column to upper just in case, though usually it is 'name'
# Check for ADLER
target = df[df['name'] == 'ADLER']

if not target.empty:
    print("\nAdler Data:")
    print(target.to_string())
    
    adler_count = target.iloc[0]['count']
    adler_rank = target.iloc[0]['rank']
    
    # Calculate difference in count
    df['count_diff'] = (df['count'] - adler_count).abs()
    
    # Sort by count difference
    # We want 12 closest.
    closest = df.sort_values('count_diff').head(20) # Get top 20 to filter
    
    print("\nClosest Matches:")
    print(closest[['name', 'rank', 'count', 'prop100k', 'count_diff']].to_string())
else:
    print("ADLER not found")
