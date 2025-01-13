from modules.osm.OSMQueryFactory import OSMQueryFactory
from modules.osm.OverpassApi import OverpassAPI
from modules.osm.OSMViewer import OSMViewer
from modules.PlaceKeywordExtractor import PlaceKeywordExtractor
from modules.utils import *
from modules.poi_clusters import *
from collections import defaultdict

factory = OSMQueryFactory()
extractor = PlaceKeywordExtractor()
api = OverpassAPI()
city = "Kraków"

def eval(profile, docType, idx):
    with open(getFilePath(profile, docType, idx), 'r') as file:
        text = file.read()

    text = preprocessBotConvo(text)
    keywords = extractor.extract_place_keywords_by_exact_match(text)
    print(keywords)

    keywords_similarity = extractor.extract_place_keywords_by_similarity(text)
    print(keywords_similarity)

    for city in ["Kraków", "Paris", "London"]:
        query = factory.generate_query(keywords, city)
        print(query)

        pois = api.fetch_pois(query)
        print(f"Found {len(pois)} POIs")

        # # Extract unique amenity values
        # unique_amenities_pois = {poi["tags"].get("amenity", "none") for poi in pois if "tags" in poi}

        # # Count the number of unique amenities
        # count_unique_amenities = len(unique_amenities_pois)
        # print(f"number of unique amenities: {count_unique_amenities}")

        # # pois = [poi for poi in pois if len(poi["tags"]) > 15]  ## experiment
        # pois.sort(key=lambda poi: len(poi["tags"]))  #pois with most tags?
        # pois = pois[-15:]
        # print("POIS:", *pois, sep='\n\t')
        # print(f"Reduced to {len(pois)} POIs")

        ####### DIFFERENT APROACH

        with open(f"pois{city}_output.txt", "w", encoding="utf-8") as file:
            for poi in pois[:200]:    
                file.write(str(poi))
                file.write("\n\n")  # Add a blank line between POIs

        print("POIs saved to pois_output.txt")

        # Group POIs by amenity
        amenity_groups = defaultdict(list)
        for poi in pois:
            amenity = poi["tags"].get("amenity", "none")
            amenity_groups[amenity].append(poi)

        # Sort each group by the number of tags in descending order
        for amenity, group in amenity_groups.items():
            group.sort(key=lambda poi: len(poi["tags"]), reverse=True)

        # Collect at least 2 POIs from each amenity group
        selected_pois = []
        for group in amenity_groups.values():
            selected_pois.extend(group[:3])  # At least 2 from each group

        # Fill remaining slots to reach 15, prioritizing POIs with the most tags
        remaining_slots = 20 - len(selected_pois)
        if remaining_slots > 0:
            # Flatten and sort all remaining POIs by the number of tags
            remaining_pois = [poi for group in amenity_groups.values() for poi in group[3:]]
            remaining_pois.sort(key=lambda poi: len(poi["tags"]), reverse=True)

            # Add the top remaining POIs to the selected list
            selected_pois.extend(remaining_pois[:remaining_slots])

        # Ensure the result has exactly 15 POIs
        selected_pois = selected_pois[:20]

        print(f"Selected {len(selected_pois)} POIs with diverse amenities.")
        print(f"Unique amenities in selected POIs: {set(poi['tags'].get('amenity', 'none') for poi in selected_pois)}")

        ########## END FOR DIFFERENT APROACH


        print("Clustering...")
        clustered_pois = cluster_pois(selected_pois, number_of_days=3)
        print("DONE")

        print("Making map...")
        viewer = OSMViewer(clustered_pois, city)
        viewer.create_map()
        #viewer.save_map(getResultMapPath(profile, docType, idx, city))
        viewer.save_map(f"{city}map.html")


if __name__ == '__main__':
    #data_preferences_types = ["cultural", "entertainment", "sport"]
    data_preferences_types = ["cultural"]
    #data_input_types = ["doc", "que", "soc"]
    data_input_types = ["doc"]

    for preference_type in data_preferences_types:
        for input_type in data_input_types:
            eval(preference_type, input_type, 0)
