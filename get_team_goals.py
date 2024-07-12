import pandas as pd

# Adjust display options for pandas
pd.options.display.max_rows = 9999
pd.options.display.max_columns = None
pd.options.display.width = 1000
pd.options.display.colheader_justify = 'left'


def get_total_goals(df):
    # Sort the DataFrame by 'goals per game' descending (adjust sorting criteria as needed)
    data = df.sort_values(by=['goals per game'], na_position='last', ascending=False)

    # Select relevant columns for skill score calculation
    data_selected = data[['player name', 'goals', 'assists', 'team name']]

    # Calculate team total goals
    team_goals = data_selected.groupby('team name')['goals'].transform('sum')

    # Calculate goal participation dynamically
    try:
        data_selected['goal_participation'] = round(
        ((data_selected['goals'] + data_selected['assists']) / team_goals) * 100, 2)
        # Return goal participation values as a list
        return data_selected['goal_participation'].tolist()
    except Exception as e:
        print(f"ERROR HELPO WHY: {e}")
        return "FUck you"
