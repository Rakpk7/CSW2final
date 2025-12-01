from cyber_db import get_it_incidents_df

df = get_it_incidents_df()
print(df)
print("Rows in IT table:", len(df))