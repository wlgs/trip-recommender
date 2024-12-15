from modules.osm.OverpassApi import OverpassAPI
import folium

class OSMViewer:
    def __init__(self, pois, city_name):
        self.pois = pois
        self.city_name = city_name
        self.map = None

    def create_map(self):
        if self.pois:
            initial_location = [self.pois[0]['lat'], self.pois[0]['lon']]
        else:
            initial_location = [50.061, 19.938]

        self.map = folium.Map(location=initial_location, zoom_start=13)

        for poi in self.pois:
            name = poi['tags'].get('name', 'Unnamed')
            lat = poi['lat']
            lon = poi['lon']
            folium.Marker(
                location=[lat, lon],
                popup=f"{name} ({lat}, {lon})",
                tooltip=name,
                icon=folium.Icon(color='blue')
            ).add_to(self.map)

    def save_map(self, filename="map.html"):
        if self.map:
            self.map.save(filename)
            print(f"Map has been saved to {filename}")
        else:
            print("Map has not been created yet.")

# Example Usage
if __name__ == "__main__":
    api = OverpassAPI()
    city = "Kraków"

    try:
        area_id = api.get_city_area_id(city)
        print(f"Area ID for {city}: {area_id}")

        query = f"""
        [out:json][timeout:25];
        (
            area({area_id})->.searchArea;
            node[amenity="library"](area.searchArea);
        );
        out center body;
        >;
        out skel qt;
        """

        pois = api.fetch_pois(query)
        print(f"Found {len(pois)} POIs")

        viewer = OSMViewer(pois, city)
        viewer.create_map()
        viewer.save_map("krakow_pois.html")

    except Exception as e:
        print(e)