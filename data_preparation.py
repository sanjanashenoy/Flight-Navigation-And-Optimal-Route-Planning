import pandas as pd

# Load the cleaned dataset
df = pd.read_csv('cleaned_routes.csv')

# Calculate predicted delay (example: random delay between 0 and 60 minutes)
import numpy as np
df['Predicted_Delay'] = np.random.randint(0, 61, size=len(df))  # Example: Random delay between 0 and 60 minutes

# Save the modified dataset
df.to_csv('cleaned_routes_with_predicted_delay.csv', index=False)
