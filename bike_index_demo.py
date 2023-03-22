"""
Author: Tyler J. Burgee
Date: 26 March 2023
Course: CIS 321 - Data & File Structure
"""

# IMPORT MODULES
from bike_index import BikeIndex

if __name__ == "__main__":
    # INSTANTIATE BikeIndex OBJECT
    bi = BikeIndex()

    # GET USER INPUT
    location = input("Enter Location to Search for Stolen Bikes: ")

    print("Searching for stolen bikes in {}...".format(location))
    search_result = bi.search_by_location(location)

    ids = bi.get_ids(search_result)
    print("Received {} stolen bikes.".format(len(ids)))

    print("Now getting their pictures...")
    bikes = bi.search_by_id(ids)
    num_received = bi.get_images(bikes)
    print("Received {} pictures, saved the files to current directory.".format(
        num_received))
