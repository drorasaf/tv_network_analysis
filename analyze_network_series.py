import pandas as pd
import datetime

df = pd.read_csv('channel_series.csv')
print (df[df['siteRating'] == 0])
df['firstAired'] = pd.to_datetime(df['firstAired'])
df = df[df['firstAired'] > datetime.datetime(2014, 1, 1)]
grouped = df.groupby('network')
count = grouped['network'].count()
networks = [count.index[i] for i in range(count.shape[0]) if count.values[i] > 4]
adjusted_df = df[df['network'].isin(networks)]
grouped = adjusted_df.groupby('network')
result_df = pd.DataFrame()
result_df['min'] = grouped['siteRating'].min()
result_df['max'] = grouped['siteRating'].max()
result_df['median'] = grouped['siteRating'].median()
result_df['mean'] = grouped['siteRating'].mean()
result_df['std'] = grouped['siteRating'].std()

print (result_df)
