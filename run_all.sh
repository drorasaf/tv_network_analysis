#/bin/bash
set -e
# create_channel_db.py

python create_channel_df.py

python analyze_network_series.py
