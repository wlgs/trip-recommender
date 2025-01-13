import requests
from collections import defaultdict

def get_wikipedia_pageviews(lang, page_name, start_date, end_date):
    """Fetch monthly Wikipedia pageviews for a specific article."""
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{lang}.wikipedia.org/all-access/user/{page_name}/monthly/{start_date}/{end_date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        total_views = sum(item['views'] for item in data['items'])
        return total_views
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wikipedia data for {lang}:{page_name} - {e}")
        return 0  # Default to 0 views if there's an issue

def rank_pois_by_popularity(pois, start_date, end_date):
    """Rank POIs by popularity using Wikipedia views or number of tags."""
    ranked_pois = []
    for poi in pois:
        tags = poi.get("tags", {})
        popularity_score = 0

        # Check for Wikipedia tag
        if "wikipedia" in tags:
            wikipedia = tags["wikipedia"]
            if ":" in wikipedia:
                lang, page_name = wikipedia.split(":", 1)
                pageviews = get_wikipedia_pageviews(lang, page_name, start_date, end_date)
                popularity_score = pageviews  # Use Wikipedia views as the metric
                print(f"Wikipedia views for {lang}:{page_name}: {popularity_score}")
        else:
            # Fallback: Use number of tags as a metric
            popularity_score = len(tags)

        # Add to the ranked list
        ranked_pois.append((popularity_score, poi))

    # Sort by popularity score in descending order
    ranked_pois.sort(reverse=True, key=lambda x: x[0])

    # Return only the POI objects, sorted by popularity
    return [poi for _, poi in ranked_pois]

# Example usage
pois = api.fetch_pois(query)  # Assume this fetches the POIs
start_date = "20231201"
end_date = "20231231"
ranked_pois = rank_pois_by_popularity(pois, start_date, end_date)

print(f"Top POIs ranked by popularity: {len(ranked_pois)}")