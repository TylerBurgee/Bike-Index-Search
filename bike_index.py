"""
Author: Tyler J. Burgee
Date: 26 March 2023
Course: CIS 321 - Data & File Structure
"""

# IMPORT MODULES
import requests
import json
import shutil

class BikeIndex:
    """Class to interface with the Bike Index REST API"""

    def __init__(self) -> None:
        """Defines the constructor for a BikeIndex object"""
        self.url = "https://bikeindex.org:443/api/v3/"

    def search_by_location(self, location: str) -> dict:
        """Performs a search query that filters results based on location stolen"""
        url = "{}search?page=1&per_page=25&location={}&distance=10&stolenness=proximity".format(self.url, location)
        response = requests.get(url)

        search_result = json.loads(response.text)

        return search_result

    def get_ids(self, search_result: dict) -> list:
        """Returns the ids of bikes within a search result"""
        ids = []

        for bike in search_result["bikes"]:
            ids.append(bike["id"])

        return ids

    def search_by_id(self, ids: list) -> list:
        """Performs a search query that filters results based on bike id"""
        bikes = []

        for bike_id in ids:
            url = "{}bikes/{}".format(self.url, bike_id)
            response = requests.get(url)
            search_result = json.loads(response.text)
            bikes.append(search_result)

        return bikes

    def get_images(self, bikes: list) -> int:
        """
        Saves images associated with given bike ids to local machine,
        Returns the number of images saved
        """
        num_received = 0
        for bike in bikes:
            for image in bike["bike"]["public_images"]:
                response = requests.get(image["full"], stream = True)
                filename = "{}.jpg".format(image["name"])

                if response.status_code == 200:
                    with open(filename, "wb") as file:
                        shutil.copyfileobj(response.raw, file)
                        num_received += 1
                        break
                else:
                    break
        return num_received

if __name__ == "__main__":
    # INSTANTIATE BikeIndex OBJECT
    bi = BikeIndex()
    location = "Maryland"

    print("Searching for stolen bikes in {}...".format(location))
    search_result = bi.search_by_location(location)

    ids = bi.get_ids(search_result)
    print("Received {} stolen bikes.".format(len(ids)))

    print("Now getting their pictures...")
    bikes = bi.search_by_id(ids)
    num_received = bi.get_images(bikes)
    print("Received {} pictures, saved the files to current directory.".format(
        num_received))
