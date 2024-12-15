from modules.osm.OSMQueryFactory import OSMQueryFactory
from modules.osm.OverpassApi import OverpassAPI
from modules.osm.OSMViewer import OSMViewer
from modules.PlaceKeywordExtractor import PlaceKeywordExtractor
from modules.utils import *

def eval(profile, docType, idx):
    with open(getFilePath(profile, docType, idx), 'r') as file:
        text = file.read()

    text = preprocessBotConvo(text)
    keywords = extractor.extract_place_keywords_by_exact_match(text)
    print(keywords)

    keywords_similarity = extractor.extract_place_keywords_by_similarity(
        text)
    print(keywords_similarity)

    for city in ["Kraków", "Paris", "New York City"]:
        query = factory.generate_query(keywords, city)
        print(query)

        pois = api.fetch_pois(query)
        print(f"Found {len(pois)} POIs")

        viewer = OSMViewer(pois, city)
        viewer.create_map()
        viewer.save_map(getResultMapPath(profile, docType, idx, city))


if __name__ == '__main__':
    factory = OSMQueryFactory()
    extractor = PlaceKeywordExtractor()
    api = OverpassAPI()
    city = "Kraków"

    data_preferences_types = ["cultural", "entertainment", "sport"]
    data_input_types = ["doc", "que", "soc"]

    for preference_type in data_preferences_types:
        for input_type in data_input_types:
            try:
                eval(preference_type, input_type, 0)
            except:
                pass
