from modules.osm.OSMQueryFactory import OSMQueryFactory
from modules.osm.OverpassApi import OverpassAPI
from modules.osm.OSMViewer import OSMViewer
from modules.PlaceKeywordExtractor import PlaceKeywordExtractor
from modules.utils import getFilePath, preprocessBotConvo

if __name__ == '__main__':
    factory = OSMQueryFactory()
    extractor = PlaceKeywordExtractor()
    api = OverpassAPI()
    city = "Kraków"

    with open(getFilePath("cultural", "doc", 0), 'r') as file:
        text = file.read()
        text = preprocessBotConvo(text)
        keywords = extractor.extract_place_keywords_by_exact_match(text)
        print(keywords)
        keywords_similarity = extractor.extract_place_keywords_by_similarity(
            text)
        print(keywords_similarity)
        query = factory.generate_query(keywords, city)
        print(query)
        pois = api.fetch_pois(query)
        #pois = [poi for poi in pois if poi['tags'].get('name')]
        print(f"Found {len(pois)} POIs")
        viewer = OSMViewer(pois, city)
        viewer.create_map()
        viewer.save_map("cultural_doc_0.html")
        
