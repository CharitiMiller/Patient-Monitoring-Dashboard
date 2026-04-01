# Chariti Miller
# IT 140 Module Six Milestone
# Simplified Dragon Text Game

# A dictionary for the simplified dragon text game
# The dictionary links a room to other rooms.
rooms = {
    'Great Hall': {'South': 'Bedroom'},
    'Bedroom': {'North': 'Great Hall', 'East': 'Cellar'},
    'Cellar': {'West': 'Bedroom'}
}

# Start the player in the Great Hall
current_room = 'Great Hall'

# Gameplay loop
while current_room != 'exit':
    # Display the player's current room
    print(f'\nYou are in the {current_room}')
    print('Enter your move: go North, go South, go East, go West, or exit')

    # Get player command
    command = input('> ')

    # Exit command
    if command == 'exit':
        current_room = 'exit'
        print('Thanks for playing!')

    # Move commands
    elif command.startswith('go '):
        direction = command[3:]  # Gets direction after "go "

        # Check if the direction is valid for the current room
        if direction in rooms[current_room]:
            current_room = rooms[current_room][direction]
            print(f'You move to the {current_room}.')
        else:
            print("You can't go that way.")

    # Invalid command
    else:
        print('Invalid command.')