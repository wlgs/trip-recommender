import spacy
from typing import List
import numpy as np


class PlaceKeywordExtractor:
    def __init__(self):
        self.nlp = spacy.load('pl_core_news_lg')

        self.place_keywords = [
            # Instytucje kultury
            'muzeum', 'galeria', 'teatr', 'kino', 'biblioteka', 'opera',

            # Miejsca handlowe
            'sklep', 'supermarket', 'centrum handlowe', 'market', 'butik',
            'antykwariat', 'salon', 'księgarnia',

            # Miejsca publiczne
            'plac', 'park', 'skwer', 'rynek', 'bulwar', 'deptak',

            # Miejsca przyrodnicze
            'łąka', 'las', 'góra', 'jezioro', 'rzeka', 'plaża',

            # Obiekty zabytkowe i historyczne
            'zamek', 'pałac', 'ruiny', 'zabytek', 'pomnik',

            # Miejsca sakralne
            'kościół', 'synagoga', 'klasztor', 'świątynia',

            # Miejsca rozrywki i rekreacji
            'klub', 'pub', 'restauracja', 'kawiarnia', 'bar', 'siłownia',
            'stadion', 'basen', 'boisko',

            # Inne specyficzne miejsca
            'dworzec', 'lotnisko', 'port', 'biblioteka', 'szkoła',
            'uniwersytet', 'uczelnia'
        ]

    def preprocess_text(self, text: str) -> tuple[List[str], List[str]]:
        doc = self.nlp(text.lower())

        tokens = [
            token.lemma_ for token in doc
            if not token.is_stop and
            not token.is_punct and
            token.is_alpha and
            len(token.lemma_) > 2
        ]

        custom_places = [
            ent.text.lower()
            for ent in doc.ents
            if ent.label_ in ['LOC', 'ORG', "persName"]
        ]

        return tokens, custom_places

    def extract_place_keywords_by_exact_match(self, text: str, max_keywords: int = 5) -> List[str]:
        tokens, custom_places = self.preprocess_text(text)

        found_places = [
            keyword for keyword in self.place_keywords
            if keyword in tokens
        ]

        unique_places = list(dict.fromkeys(found_places))
        unique_places.extend(custom_places)
        return unique_places[:max_keywords]

    def extract_place_keywords_by_similarity(self, text: str, max_keywords: int = 5) -> List[str]:
        # Utwórz obiekt Doc dla tekstu wejściowego
        doc = self.nlp(text.lower())

        # Jeśli doc jest pusty lub model nie rozpoznał sensownego wektora, zwróć pustą listę
        if not doc.vector_norm:
            return []

        # Obliczanie podobieństwa tekstu do każdego słowa kluczowego
        keyword_similarities = []
        for keyword in self.place_keywords:
            keyword_doc = self.nlp(keyword)

            # Obliczanie podobieństwa między wektorami
            similarity = doc.similarity(keyword_doc)
            keyword_similarities.append((keyword, similarity))

        # Sortowanie wyników po podobieństwie (malejąco)
        keyword_similarities.sort(key=lambda x: x[1], reverse=True)
        print(keyword_similarities)

        # Pobieranie maksymalnie `max_keywords` najlepszych słów kluczowych
        best_keywords = [keyword for keyword,
                         _ in keyword_similarities[:max_keywords]]
        return best_keywords
