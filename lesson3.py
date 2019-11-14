import pandas as pd

enemy_table_df = pd.DataFrame(enemy_table, columns = ranges.keys())
print(enemy_table_df)

enemy_table_df.to_csv('enemy_table.csv')