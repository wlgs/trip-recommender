from modules.osm.OSMQueryFactory import OSMQueryFactory
from modules.osm.OverpassApi import OverpassAPI
from modules.osm.OSMViewer import OSMViewer
from modules.PlaceKeywordExtractor import PlaceKeywordExtractor
from modules.utils import *
from modules.poi_clusters import *
from collections import defaultdict
from wikipedia_popularity import *

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

    for city in ["Kraków"]:
        query = factory.generate_query(keywords, city)
        print(query)

        pois = api.fetch_pois(query)
        print(f"Found {len(pois)} POIs")

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
            selected_pois.extend(group[:10])  # At least 5 from each group

        # # Fill remaining slots to reach 15, prioritizing POIs with the most tags
        # remaining_slots = 20 - len(selected_pois)
        # if remaining_slots > 0:
        #     # Flatten and sort all remaining POIs by the number of tags
        #     remaining_pois = [poi for group in amenity_groups.values() for poi in group[3:]]
        #     remaining_pois.sort(key=lambda poi: len(poi["tags"]), reverse=True)

        #     # Add the top remaining POIs to the selected list
        #     selected_pois.extend(remaining_pois[:remaining_slots])

        # # Ensure the result has exactly 15 POIs
        # selected_pois = selected_pois[:20]

        selected_pois_ranked = rank_pois_by_popularity(selected_pois, 20241201, 20241231)
        selected_pois_ranked = selected_pois_ranked[:10]

        print(f"Selected {len(selected_pois_ranked)} POIs with diverse amenities.")
        print(f"Unique amenities in selected POIs: {set(poi['tags'].get('amenity', 'none') for poi in selected_pois_ranked)}")

        ########## END FOR DIFFERENT APROACH


        print("Clustering...")
        clustered_pois = cluster_pois(selected_pois_ranked, number_of_days=3)
        print("DONE")

        print("Making map...")
        viewer = OSMViewer(clustered_pois, city)
        viewer.create_map()
        #viewer.save_map(getResultMapPath(profile, docType, idx, city))
        viewer.save_map(f"{city}map.html")


if __name__ == '__main__':
    #data_preferences_types = ["cultural", "entertainment", "sport"]
    # data_preferences_types = ["cultural"]
    #data_input_types = ["doc", "que", "soc"]
    # data_input_types = ["doc"]

    # for preference_type in data_preferences_types:
    #     for input_type in data_input_types:
    #         eval(preference_type, input_type, 0)
    eval("entertainment", "que", 0)
