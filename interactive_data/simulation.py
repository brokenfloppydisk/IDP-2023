import random
import csv
# import matplotlib.pyplot as plt
# from matplotlib import animation

# fig, ax = plt.subplots(figsize=(10, 10))
# stored_water, = ax.plot([], [], lw=5, c="blue")

# Variables
filename = "data.csv"


def liters_to_gal(liters: float) -> float:
    return liters / 3.78541


# Time
FLIGHT_DAYS: int = 214
COLONY_DAYS: int = 3650

NUM_PEOPLE = 20

# ISS has 1920 liters of water for 7 people for 3 months
# https://ntrs.nasa.gov/api/citations/20180006341/downloads/20180006341.pdf
START_WATER = (7/3) * liters_to_gal(1920 * (NUM_PEOPLE / 7))

# https://www.nasa.gov/sites/default/files/atoms/files/mars_ice_drilling_assessment_v6_for_public_release.pdf
MAX_WATER_STORED = (NUM_PEOPLE) * liters_to_gal(1000 * 20)

# Total Water Lost
total_water_used: float = 0
total_water_lost: float = 0
total_water_recycled: float = 0
recycle_percentage: float = 0.85
water_stored: float = START_WATER

# Water Extraction
total_water_gained: int = 0

# Simulation
current_water = 0


def get_recycle_percentage() -> float:
    """
    Returns 75% - 85%
    """
    return recycle_percentage + (random.random() * 0.1) - 0.05


# Returns a random percentage between 1-5% to indicate alteration
def get_water_deviation() -> float:
    #-5% to 5% deviation
    return random.random() * 0.1 - 0.05

    # Returns the water usage for an individual with the alterations accounted for


def get_individual_water_usage(base_water: float) -> float:
    return base_water * (1 + get_water_deviation())


def get_individual_space_water_usage() -> "tuple[float, float]":
    water_used = 0
    water_recycled = 0

    # ISS Astronauts use 3 gal per day
    water_used = 3
    water_used *= (1 + get_water_deviation())
    water_recycled = get_recycle_percentage() * water_used

    return (water_used, water_recycled)

def simulate() -> None:
    water_mined_per_day = int(
        input("How much water should be mined per day (in Gallons)? "))

    global total_water_used
    global total_water_lost
    global total_water_recycled
    global total_water_gained
    global water_stored
    total_water_used = 0
    total_water_lost = 0
    total_water_recycled = 0
    total_water_gained = 0
    water_stored = 0

    # Open the CSV file in write mode and create a CSV writer
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Day", "Water Stored", "Water Used Today", "Water Gained Today",
                        "Water Lost Today", "Water Recycled Today",
                        "Total Water Used", "Total Water Lost",
                        "Total Water Gained", "Total Water Recycled"])

        water_stored = START_WATER

        # During Flight
        for day in range(1, FLIGHT_DAYS + 1):
            water_used_today = 0
            water_lost_today = 0
            water_recycled_today = 0

            for x in range(NUM_PEOPLE):
                individual_water, individual_recycled = get_individual_space_water_usage()
                water_used_today += individual_water
                water_recycled_today += individual_recycled

            water_lost_today = water_used_today - water_recycled_today

            total_water_used += water_used_today
            total_water_lost += water_lost_today
            total_water_recycled += water_recycled_today

            water_stored -= water_lost_today

            # Save the data
            writer.writerow([day, water_stored, water_used_today, 0,
                            water_lost_today, water_recycled_today,
                            total_water_used, total_water_lost,
                            total_water_gained, total_water_recycled])

            # print(f"Day: {day} | Water Left: {water_stored} L | Water Used: {water_used_today} | ", end="")
            # print(f"Water Lost: {water_lost_today} L | Water Recycled: {water_recycled_today} | ", end="")
            # print(f"Total Water Used: {total_water_used} L | Total Water Lost: {total_water_lost} | ", end="")
            # print(f"Total Water Gained: {total_water_gained} L | Total Water Recycled: {total_water_recycled}")
        
        print("\nSpace water statistics: ")
        print(f"Water left in storage: {water_stored:.2f}")
        print(f"Total Water Used: {total_water_used:.2f} L | Total Water Lost: {total_water_lost:.2f}")
        print(f"Total Water Gained: {total_water_gained:.2f} L | Total Water Recycled: {total_water_recycled:.2f}")

        colonization_water_used = 0.0
        colonization_water_lost = 0.0
        colonization_water_gained = 0.0
        colonization_water_recycled = 0.0

        # During Colonization
        for day in range(1, COLONY_DAYS + 1):
            water_used_today = 0
            water_lost_today = 0
            water_recycled_today = 0

            for x in range(NUM_PEOPLE):
                individual_water = get_individual_water_usage(65.5)
                water_used_today += individual_water
                water_recycled_today += individual_water * get_recycle_percentage()

            water_lost_today = water_used_today - water_recycled_today

            water_gained_today = water_mined_per_day

            colonization_water_lost += (water_lost_today)
            colonization_water_used += water_used_today
            colonization_water_recycled += water_recycled_today
            colonization_water_gained += water_gained_today

            water_stored += water_gained_today - water_lost_today
            # Stop water stored from exceeding max
            water_stored = min(water_stored, MAX_WATER_STORED)

            # Print daily statistics
            writer.writerow([day, water_stored, water_used_today, water_gained_today,
                            water_lost_today, water_recycled_today,
                            colonization_water_gained, colonization_water_lost,
                            colonization_water_gained, colonization_water_recycled])

        total_water_lost += colonization_water_lost
        total_water_used += colonization_water_used
        total_water_recycled += colonization_water_recycled
        total_water_gained += colonization_water_gained

        print("\nColonization water statistics: ")
        print(f"Water left in storage: {water_stored:.2f}")
        print(f"Colonization Water Used: {colonization_water_used:.2f} L | Colonization Water Lost: {colonization_water_lost:.2f}")
        print(f"Colonization Water Gained: {colonization_water_gained:.2f} L | Colonization Water Recycled: {colonization_water_recycled:.2f}")
        
        print("\nTotal statistics: ")
        print(f"Water left in storage: {water_stored:.2f}")
        print(f"Total Water Used: {total_water_used:.2f} L | Total Water Lost: {total_water_lost:.2f}")
        print(f"Total Water Gained: {total_water_gained:.2f} L | Total Water Recycled: {total_water_recycled:.2f}")


simulate()