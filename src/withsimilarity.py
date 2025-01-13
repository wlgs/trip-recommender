from modules.osm.OSMQueryFactory import OSMQueryFactory
from modules.osm.OverpassApi import OverpassAPI
from modules.osm.OSMViewer import OSMViewer
from modules.PlaceKeywordExtractor import PlaceKeywordExtractor
from modules.utils import *

factory = OSMQueryFactory()
extractor = PlaceKeywordExtractor()
api = OverpassAPI()
city = "Kraków"

MAX_POIS = 20

def eval(profile, docType, idx):
    with open(getFilePath(profile, docType, idx), 'r') as file:
        text = file.read()

    keywords_similarity = extractor.extract_place_keywords_by_similarity(text)
    print(keywords_similarity, sep="\n")

    for city in ["Kraków", "Paris", "London"]:
        all_pois = []
        for keyword, similarity in keywords_similarity:
            query = factory.generate_query(keyword, city)
            print(query)

            pois = api.fetch_pois(query)
            print(f"Found {len(pois)} POIs for keyword: {keyword}")
            pois.sort(key=lambda poi: len(poi["tags"]))
            pois = pois[-int(similarity*MAX_POIS):]
            print(f"Reduced to {len(pois)} POIs")
            all_pois.extend(pois)

        viewer = OSMViewer([all_pois], city)
        viewer.create_map()
        viewer.save_map(f"result_{city}.html")


if __name__ == '__main__':
    #data_preferences_types = ["cultural", "entertainment", "sport"]
    data_preferences_types = ["cultural"]
    #data_input_types = ["doc", "que", "soc"]
    data_input_types = ["doc"]

    for preference_type in data_preferences_types:
        for input_type in data_input_types:
            try:
                eval(preference_type, input_type, 0)
            except:
                pass
