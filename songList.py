import pandas as pd
tables=[]
for i in range(97, 123):#a to z
    url = f'https://bollywoodproduct.in/complete-list-of-bollywood-songs-alphabetically-from-{chr(i)}/'
    table = pd.read_html(url)
    tables.append(table)
combined = pd.concat([t[0] for t in tables], axis=0)
combined.reset_index(drop=True, inplace=True)
combined.to_csv('combined.csv', index=False)
