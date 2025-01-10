import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
csv_path =  "/Users/filipberntsson/Documents/Studies/Courses/game_theory_and_rationality/Project/BestVersion/results_all_sorted.csv" # Replace with the actual path to your CSV
data = pd.read_csv(csv_path)

# Extract unique values of R
unique_R = sorted(data["R"].unique())
num_plots = len(unique_R)

# Initialize the plot index
current_plot_index = 0

# Function to create the heatmap for a given index
def plot_heatmap(index):
    global current_plot_index

    # Clamp the index to stay within bounds
    current_plot_index = max(0, min(index, num_plots - 1))

    # Clear the current plot
    plt.clf()

    # Get the current R
    r = unique_R[current_plot_index]

    # Filter data for the current R
    subset = data[data["R"] == r]

    # Create a pivot table for the heatmap
    heatmap_data = subset.pivot_table(
        index="M_A",
        columns="M_B",
        values="NumPureNashEquilibria",  # Adjust to match the column in your CSV
        aggfunc="sum",
        fill_value=0
    )

    # Plot the heatmap
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="viridis", cbar=True)
    plt.title(f"Heatmap of Nash Equilibria Counts for R={r}")
    plt.xlabel("M_B")
    plt.ylabel("M_A")
    plt.tight_layout()
    plt.draw()  # Update the plot

# Function to handle key press events
def on_key(event):
    global current_plot_index
    if event.key == "right":  # Forward
        plot_heatmap(current_plot_index + 1)
    elif event.key == "left":  # Backward
        plot_heatmap(current_plot_index - 1)

# Set up the figure
plt.figure(figsize=(10, 8))

# Connect the key press event to the handler
plt.gcf().canvas.mpl_connect("key_press_event", on_key)

# Plot the initial heatmap
plot_heatmap(current_plot_index)

# Show the plotpip
plt.show()
