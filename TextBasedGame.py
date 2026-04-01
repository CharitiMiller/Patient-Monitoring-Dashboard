# Name: Chariti Miller

# Function to display instructions
def show_instructions():
    print("🏡 Farmhouse Adventure Game")
    print("Collect all 6 items before entering the Final Room!")
    print("Commands:")
    print("  go North, go South, go East, go West")
    print("  get [item name]")
    print("----------------------------------")


# Function to display player status
def show_status(current_room, inventory, rooms):
    print("\n---------------------------")
    print("You are in:", current_room)
    print("Inventory:", inventory)

    # Show item in room if exists
    if "item" in rooms[current_room]:
        print("You see a:", rooms[current_room]["item"])
    print("---------------------------")


def main():
    # Dictionary of rooms and items
    rooms = {
        "Living Room": {"North": "Kitchen", "East": "Bedroom", "West": "Office"},
        "Kitchen": {"South": "Living Room", "item": "Key"},
        "Bedroom": {"West": "Living Room", "North": "Bathroom", "item": "Blanket"},
        "Bathroom": {"South": "Bedroom", "item": "Towel"},
        "Office": {"East": "Living Room", "North": "Garage", "item": "Laptop"},
        "Garage": {"South": "Office", "East": "Final Room", "item": "Flashlight"},
        "Final Room": {"West": "Garage", "item": "Villain"}  # Villain room
    }

    current_room = "Living Room"
    inventory = []

    show_instructions()

    # Gameplay loop
    while True:
        show_status(current_room, inventory, rooms)

        # Check for loss (enter villain room too early)
        if current_room == "Final Room":
            if len(inventory) < 6:
                print("💀 NOM NOM... GAME OVER!")
                print("You entered the final room without all items.")
                break
            else:
                print("🎉 Congratulations! You collected all items and won!")
                break

        move = input("Enter your move: ").strip()

        # Movement command
        if move.lower().startswith("go "):
            direction = move.split()[1].capitalize()

            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                print("❌ You can't go that way!")

        # Get item command
        elif move.lower().startswith("get "):
            item = move[4:]

            if "item" in rooms[current_room] and item.lower() == rooms[current_room]["item"].lower():
                inventory.append(rooms[current_room]["item"])
                print("✅ You picked up:", rooms[current_room]["item"])
                del rooms[current_room]["item"]
            else:
                print("❌ No such item here!")

        # Invalid command
        else:
            print("❌ Invalid command!")

    print("\nThanks for playing!")


# Run the game
main()