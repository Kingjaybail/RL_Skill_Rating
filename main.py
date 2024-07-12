import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from get_team_goals import get_total_goals

def open_file():
    # Open file dialog and get file path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8')

    # Process data and calculate skill score
    data = df.sort_values(by=['goals per game'], na_position='last', ascending=False)
    data_selected = data[['player name', 'win percentage', 'score per game', 'goals per game', 'assists per game',
                          'saves per game', 'shooting percentage', 'goals conceded while last defender per game',
                          'bpm per game', '0 boost time per game', 'avg boost amount per game',
                          'amount used while supersonic per game', 'avg speed per game', 'time slow speed per game',
                          'time powerslide per game', 'demos inflicted per game', 'demos taken per game']]

    data_selected['goal_participation'] = get_total_goals(df)

    data_selected['skill_score'] = (
        (data_selected['win percentage'] * 17) +
        (data_selected['score per game'] * 15) +
        (data_selected['goals per game'] * 15) +
        (data_selected['assists per game'] * 15) +
        (data_selected['saves per game'] * 15) +
        (data_selected['shooting percentage'] * 15) +
        (data_selected['goals conceded while last defender per game'] * -5) -
        (data_selected['bpm per game'] + 0) -
        (data_selected['0 boost time per game'] + 0) +
        (data_selected['avg boost amount per game'] * 10) +
        (data_selected['amount used while supersonic per game'] * -3) +
        (data_selected['avg speed per game'] * 3) +
        (data_selected['time slow speed per game'] * -10) +
        (data_selected['time powerslide per game'] * 5) +
        (data_selected['demos inflicted per game'] * 8) +
        (data_selected['demos taken per game'] * -15) +
        (data_selected['goal_participation'] * 25)
    ) / 10000

    skill_rating = data_selected[['player name', 'skill_score']].sort_values(by='skill_score', ascending=False)
    skill_rating['rank'] = range(1, len(skill_rating) + 1)

    # Print skill rating with rank
    for index, row in skill_rating.iterrows():
        print(f"{row['player name']} (Rank: {row['rank']}) - Skill Score: {row['skill_score']:.2f}")

    # Create a bar plot
    plt.figure(figsize=(10, 5))
    sns.barplot(x='skill_score', y='player name', data=skill_rating)
    plt.title('Skill Score by Player')
    plt.xlabel('Skill Score')
    plt.ylabel('Player Name')

    # Clear previous plot
    for widget in frame_plot.winfo_children():
        widget.destroy()

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Show the plot
    plt.close()

# Set up the Tkinter window
root = tk.Tk()
root.title("Skill Score Plotter")
root.geometry("1280x720")

# Create a frame for the plot
frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a separate frame for the button
frame_button = tk.Frame(root)
frame_button.pack(side=tk.BOTTOM, pady=10)

# Create a button to open the file dialog
btn_open_file = tk.Button(frame_button, text="Open CSV File", command=open_file)
btn_open_file.pack()

# Start the Tkinter main loop
root.mainloop()
