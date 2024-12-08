from PlaceKeywordExtractor import PlaceKeywordExtractor
from OSMQueryFactory import OSMQueryFactory
from utils import getFilePath, preprocessBotConvo

if __name__ == '__main__':
    factory = OSMQueryFactory()
    extractor = PlaceKeywordExtractor()

    with open(getFilePath("cultural", "doc", 0), 'r') as file:
        text = file.read()
        text = preprocessBotConvo(text)
        keywords = extractor.extract_place_keywords_by_exact_match(text)
        print(keywords)
        keywords_similarity = extractor.extract_place_keywords_by_similarity(
            text)
        print(keywords_similarity)
        query = factory.generate_query(keywords, "Kraków")
        print(query)
