def transform_input(data):
    # For now just return raw values
    return [
        data['team1'],
        data['team2'],
        data['toss_winner'],
        data['toss_decision'],
        data['venue']
    ]