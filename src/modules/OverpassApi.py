import requests

class OverpassAPI:
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"

    def __init__(self, url=OVERPASS_URL):
        self.url = url

    def send_query(self, query):
        try:
            print("Sending query to Overpass API...")
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            response = requests.post(self.url, data={'data': query.encode('utf-8')}, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error with Overpass API request: {e}")

    def fetch_pois(self, query):
        data = self.send_query(query)
        return self._process_response(data)

    def get_city_area_id(self, city_name):
        query = f"""
        [out:json][timeout:25];
        area[name="{city_name}"];
        out;
        """
        data = self.send_query(query)
        for element in data.get('elements', []):
            if element.get('type') == 'area':
                return element.get('id')
        raise Exception(f"City '{city_name}' not found or no area ID available.")

    def _process_response(self, data):
        pois = []
        for element in data.get('elements', []):
            if 'lat' in element and 'lon' in element:
                poi = {
                    "type": element.get("type"),
                    "id": element.get("id"),
                    "lat": element.get("lat"),
                    "lon": element.get("lon"),
                    "tags": element.get("tags", {})
                }
                pois.append(poi)
        return pois

# Example Usage
if __name__ == "__main__":
    overpass_api = OverpassAPI()

    city_name = "Kraków"
    try:
        area_id = overpass_api.get_city_area_id(city_name)
        print(f"Area ID for {city_name}: {area_id}")

        query = f"""
        [out:json][timeout:25];
        (
            area({area_id})->.searchArea;
            node[amenity="library"](area.searchArea);
        );
        out body;
        >;
        out skel qt;
        """

        pois = overpass_api.fetch_pois(query)
        print(f"Found {len(pois)} POIs:")
        for poi in pois:
            name = poi['tags'].get('name', 'Unnamed')
            print(f"POI: {name} - Type: {poi['type']} - Lat: {poi['lat']}, Lon: {poi['lon']}")

    except Exception as e:
        print(e)
