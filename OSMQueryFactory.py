class OSMQueryFactory:
    def __init__(self):
        # Mapa kategorii OSM do odpowiednich słów kluczowych
        self.keyword_tag_mapping = {
            'muzeum': {'amenity': ['museum']},
            'galeria': {'amenity': ['arts_centre']},
            'teatr': {'amenity': ['theatre']},
            'kino': {'amenity': ['cinema']},
            'biblioteka': {'amenity': ['library']},
            'opera': {'building': ['opera']},
            'sklep': {'shop': ['yes']},
            'supermarket': {'shop': ['supermarket']},
            'centrum handlowe': {'shop': ['mall']},
            'market': {'amenity': ['marketplace']},
            'butik': {'shop': ['boutique']},
            'antykwariat': {'shop': ['books']},
            'salon': {'shop': ['salon']},
            'księgarnia': {'shop': ['books']},
            'plac': {'place': ['square']},
            'park': {'leisure': ['park']},
            'skwer': {'place': ['square']},
            'rynek': {'place': ['square']},
            'bulwar': {'highway': ['pedestrian']},
            'deptak': {'highway': ['pedestrian']},
            'łąka': {'natural': ['meadow']},
            'las': {'natural': ['wood']},
            'góra': {'natural': ['peak']},
            'jezioro': {'natural': ['water'], 'water': ['lake']},
            'rzeka': {'waterway': ['river']},
            'plaża': {'place': ['beach']},
            'zamek': {'historic': ['castle']},
            'pałac': {'historic': ['palace']},
            'ruiny': {'historic': ['ruins']},
            'zabytek': {'historic': ['monument']},
            'pomnik': {'historic': ['monument']},
            'kościół': {'building': ['church']},
            'synagoga': {'building': ['synagogue']},
            'klasztor': {'building': ['monastery']},
            'świątynia': {'building': ['temple']},
            'klub': {'amenity': ['nightclub']},
            'pub': {'amenity': ['pub']},
            'restauracja': {'amenity': ['restaurant']},
            'kawiarnia': {'amenity': ['cafe']},
            'bar': {'amenity': ['bar']},
            'siłownia': {'leisure': ['fitness_centre']},
            'stadion': {'leisure': ['stadium']},
            'basen': {'leisure': ['swimming_pool']},
            'boisko': {'leisure': ['pitch']},
            'dworzec': {'amenity': ['bus_station']},
            'lotnisko': {'aeroway': ['aerodrome']},
            'port': {'landuse': ['harbour']},
            'szkoła': {'amenity': ['school']},
            'uniwersytet': {'amenity': ['university']},
            'uczelnia': {'amenity': ['university']}
        }

    def generate_query(self, keywords, city):
        if not isinstance(keywords, list):
            raise ValueError("Keywords must be a list.")

        query_parts = set()

        for keyword in keywords:
            # Pobierz tagi dla danego słowa kluczowego
            tags = self.keyword_tag_mapping.get(keyword)
            if not tags:
                continue  # Ignoruj nieznane słowa kluczowe

            for key, values in tags.items():
                for value in values:
                    query_parts.add(f'node[{key}="{value}"](area.searchArea);')
                    query_parts.add(f'way[{key}="{value}"](area.searchArea);')
                    query_parts.add(
                        f'relation[{key}="{value}"](area.searchArea);')

        if not query_parts:
            raise ValueError("No valid keywords provided.")

        query_body = "\n".join(query_parts)
        overpass_query = f"""
        [out:json][timeout:25];
        (
                  {{{{geocodeArea:Kraków}}}}->.searchArea;
            {query_body}
        );
        out body;
        >;
        out skel qt;
        """
        return overpass_query
