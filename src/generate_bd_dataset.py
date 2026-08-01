# -*- coding: utf-8 -*-
"""
Generates a Bangladesh-focused travel dataset in CSV format, aimed at a
Gen Z travel-recommendation project. Destinations are real BD places;
users are synthetic Gen Z personas; ratings are simulated with a
preference bias so the recommender has real signal to learn from.
"""
import csv
import random
import os

random.seed(7)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 40 real Bangladeshi destinations across all 8 divisions
# ---------------------------------------------------------------------------
DESTINATIONS = [
    # name, division, category, vibe_tags, budget_level, best_season, cost_bdt/day, insta_score(1-10), lat, lon, description
    ("Cox's Bazar Beach", "Chattogram", "beach", "sunset|beach-walk|iconic", "medium", "winter", 2500, 9, 21.4272, 92.0058,
     "World's longest natural sea beach with golden sand stretching over 120km, packed sunsets and beach shacks."),
    ("Saint Martin's Island", "Chattogram", "island", "island-hop|snorkel|hidden-gem", "high", "winter", 3500, 10, 20.6280, 92.3220,
     "BD's only coral island — turquoise water, coconut trees, and a boat ride you'll never shut up about."),
    ("Sajek Valley", "Chattogram", "hill", "cloud-chasing|instagrammable|road-trip", "medium", "winter", 2800, 10, 23.3833, 92.2833,
     "The 'Queen of Hills' — resorts sit above the clouds, literally. Sunrise here breaks the internet every time."),
    ("Bandarban (Nilgiri & Boga Lake)", "Chattogram", "hill", "trekking|adventure|offbeat", "medium", "summer", 3000, 9, 22.1953, 92.2184,
     "Steep hill trails, a crater lake at 2,900ft, and Bawm/Marma village stays for the truly adventurous."),
    ("Rangamati (Kaptai Lake)", "Chattogram", "hill", "boat-ride|hanging-bridge|chill", "low", "winter", 1800, 8, 22.6533, 92.1785,
     "Boat across a massive man-made lake, cross the iconic hanging bridge, eat bamboo chicken."),
    ("Sundarbans", "Khulna", "forest", "wildlife|royal-bengal-tiger|unesco", "high", "winter", 4000, 8, 21.9497, 89.1833,
     "The largest mangrove forest on Earth and home of the Royal Bengal Tiger — UNESCO World Heritage Site."),
    ("Kuakata Sea Beach", "Barishal", "beach", "sunrise-and-sunset|quiet|underrated", "low", "winter", 1900, 8, 21.8153, 90.1197,
     "The only beach in BD where you can watch both sunrise AND sunset over the sea — way less crowded than Cox's."),
    ("Sylhet Tea Gardens", "Sylhet", "tea-garden", "green-everything|instagrammable|chill", "low", "monsoon", 1700, 9, 24.8949, 91.8687,
     "Endless rolling tea estates in every shade of green — Srimangal and Malnicherra are the must-see gardens."),
    ("Ratargul Swamp Forest", "Sylhet", "forest", "boat-ride|hidden-gem|unique", "low", "monsoon", 1500, 9, 25.0122, 91.9553,
     "The 'Amazon of Bangladesh' — a freshwater swamp forest you explore entirely by boat through submerged trees."),
    ("Bisnakandi", "Sylhet", "waterfall", "crystal-water|hidden-gem|day-trip", "low", "monsoon", 1600, 9, 25.1958, 92.0122,
     "Crystal clear stream water rolling down from Meghalaya hills, framed by clouds — an easy day trip from Sylhet."),
    ("Jaflong", "Sylhet", "hill", "border-view|stone-collecting|scenic", "low", "monsoon", 1500, 8, 25.1622, 92.0083,
     "Stone-strewn riverbeds at the India border with the Khasi hills as a backdrop."),
    ("Tanguar Haor", "Sunamganj", "wetland", "boat-house|sunrise|off-grid", "medium", "monsoon", 2200, 9, 25.1167, 91.1167,
     "A massive wetland ecosystem — rent a houseboat and wake up in the middle of open water."),
    ("Paharpur (Somapura Mahavihara)", "Rajshahi", "heritage", "unesco|history-nerd|ancient", "low", "winter", 1400, 6, 25.0309, 88.9770,
     "Ruins of the largest known Buddhist monastery south of the Himalayas — UNESCO listed since 1985."),
    ("Mahasthangarh", "Bogura", "heritage", "ancient|archaeology|underrated", "low", "winter", 1300, 5, 24.9614, 89.3411,
     "One of the earliest urban archaeological sites in Bangladesh, dating back to 3rd century BCE."),
    ("Sonargaon (Panam City)", "Dhaka", "heritage", "abandoned-aesthetic|day-trip|photography", "low", "any", 1200, 8, 23.6497, 90.6108,
     "A ghost town of crumbling 19th-century merchant mansions — peak 'abandoned aesthetic' photo content."),
    ("Old Dhaka (Puran Dhaka)", "Dhaka", "urban", "street-food|history|chaos-core", "low", "any", 1000, 9, 23.7104, 90.4074,
     "Narrow lanes, Mughal-era architecture, and legendary street food — biryani, chui jhal, and everything in between."),
    ("Lalbagh Fort", "Dhaka", "heritage", "mughal|photography|city-escape", "low", "any", 800, 7, 23.7189, 90.3883,
     "Unfinished 17th-century Mughal fort complex right in the middle of Old Dhaka."),
    ("Ahsan Manzil (Pink Palace)", "Dhaka", "heritage", "pink-palace|instagrammable|riverside", "low", "any", 800, 8, 23.7086, 90.4058,
     "The pastel-pink former palace of the Dhaka Nawabs, sitting right on the Buriganga river."),
    ("Srimangal", "Sylhet", "tea-garden", "seven-layer-tea|nature|chill", "low", "winter", 1600, 9, 24.3065, 91.7296,
     "Tea capital of Bangladesh — famous for seven-layer tea, pineapple gardens, and the Lawachara rainforest nearby."),
    ("Lawachara National Park", "Sylhet", "forest", "hoolock-gibbon|trekking|wildlife", "low", "winter", 1500, 7, 24.3242, 91.7859,
     "Rainforest national park home to hoolock gibbons — Bangladesh's only ape species."),
    ("Himchari National Park", "Chattogram", "waterfall", "waterfall|hiking|near-coxs-bazar", "low", "winter", 1800, 7, 21.3559, 92.0217,
     "Waterfalls and hilltop viewpoints just outside Cox's Bazar — an easy half-day add-on."),
    ("Nilgiri Hills", "Bandarban", "hill", "clouds|resort-stay|scenic", "high", "winter", 3200, 10, 21.7500, 92.4167,
     "One of the highest resort points in BD — you're often standing above the cloud line."),
    ("Chimbuk Hill", "Bandarban", "hill", "roadtrip|panorama|offbeat", "medium", "winter", 2000, 8, 21.9333, 92.3167,
     "Winding hill road with panoramic Chittagong Hill Tracts views — great biking route."),
    ("Kaptai National Park", "Rangamati", "forest", "wildlife|jungle|adventure", "low", "winter", 1700, 6, 22.5000, 92.2167,
     "Dense forest reserve with elephant sightings and jungle trekking trails."),
    ("Bhimruli Floating Market", "Barishal", "wetland", "floating-market|unique|boat-tour", "low", "monsoon", 1400, 9, 22.7333, 90.2000,
     "A floating guava and vegetable market on canals — locals sell straight from wooden boats."),
    ("Sitakunda Eco Park", "Chattogram", "hill", "hiking|hot-spring|nature", "low", "winter", 1500, 6, 22.6167, 91.6667,
     "Hiking trails leading to a natural hot spring and hilltop Buddhist temple."),
    ("Kantajew Temple", "Dinajpur", "heritage", "terracotta|architecture|underrated", "low", "any", 1000, 7, 25.6833, 88.8833,
     "18th-century terracotta Hindu temple famous for its intricate carved brick panels."),
    ("Nijhum Dwip", "Noakhali", "island", "deer-spotting|off-grid|quiet", "low", "winter", 1600, 8, 22.0500, 91.0500,
     "Remote island with spotted deer roaming free — genuinely feels like the edge of the map."),
    ("Char Kukri Mukri", "Bhola", "island", "mangrove|birdwatching|off-grid", "low", "winter", 1500, 6, 21.9500, 90.7000,
     "Mangrove island sanctuary popular with birdwatchers and people who want zero phone signal."),
    ("Panam Nagar", "Narayanganj", "heritage", "abandoned-aesthetic|photography|day-trip", "low", "any", 1000, 8, 23.6483, 90.6122,
     "Row after row of decaying colonial-era merchant houses, frozen in time."),
    ("Comilla (Mainamati)", "Comilla", "heritage", "buddhist-ruins|history|underrated", "low", "any", 1200, 5, 23.4682, 91.1116,
     "Buddhist archaeological ruins spread across low hills, dating back to the 8th century."),
    ("Madhabkunda Waterfall", "Moulvibazar", "waterfall", "waterfall|swim|nature", "low", "monsoon", 1400, 8, 24.6167, 92.1333,
     "The largest waterfall in Bangladesh, tucked inside a tea-garden landscape."),
    ("Cox's Bazar - Inani Beach", "Chattogram", "beach", "coral-beach|quiet|instagrammable", "medium", "winter", 2600, 9, 21.2833, 92.0333,
     "Quieter coral-lined stretch south of the main Cox's Bazar beach — better sand, way fewer crowds."),
    ("Teknaf", "Chattogram", "beach", "border-town|hills-meet-sea|offbeat", "medium", "winter", 2400, 7, 20.8600, 92.3050,
     "Where the hills tumble straight into the sea — southernmost tip of mainland Bangladesh."),
    ("Barind Museum & Varendra Research", "Rajshahi", "heritage", "museum|history-nerd|indoor", "low", "any", 900, 5, 24.3745, 88.6042,
     "One of the oldest museums in South Asia with an impressive terracotta and sculpture collection."),
    ("Foy's Lake", "Chattogram", "urban", "theme-park|family|weekend-trip", "low", "any", 1300, 6, 22.3667, 91.7833,
     "Man-made lake with a hillside amusement park — classic Chattogram weekend spot."),
    ("Patenga Beach", "Chattogram", "beach", "sunset|city-beach|easy-access", "low", "any", 1200, 7, 22.2333, 91.7833,
     "River-meets-sea beach right at the edge of Chattogram city, best for a quick sunset fix."),
    ("Meghla Tourist Complex", "Bandarban", "hill", "lake|cable-car|family", "low", "winter", 1500, 6, 22.1833, 92.2333,
     "Artificial lake surrounded by hills with a cable car and hanging bridge — easy Bandarban intro stop."),
    ("Baldha Garden", "Dhaka", "urban", "botanical|hidden-gem|indoor", "low", "any", 500, 6, 23.7133, 90.4200,
     "A century-old botanical garden tucked inside Old Dhaka with rare plant species from around the world."),
    ("Hazrat Shahjalal Mazar", "Sylhet", "heritage", "spiritual|pigeons|local-culture", "low", "any", 900, 6, 24.8967, 91.8687,
     "Shrine of the Sufi saint who brought Islam to Sylhet — famous for its resident flock of pigeons."),
]

# ---------------------------------------------------------------------------
# Gen Z personas (18-27), across Bangladeshi cities/universities
# ---------------------------------------------------------------------------
FIRST_NAMES = ["Ayesha", "Rafi", "Nusrat", "Tanvir", "Farhan", "Mim", "Sadia", "Adnan",
               "Priyo", "Tasnim", "Rakib", "Nabila", "Shuvo", "Anika", "Imran", "Proma",
               "Zayan", "Lamia", "Fahim", "Orin", "Nafis", "Rida", "Shafin", "Meherin",
               "Arnob", "Tania", "Sabbir", "Mahi", "Rezwan", "Ishika"]

CITIES = ["Dhaka", "Chattogram", "Sylhet", "Rajshahi", "Khulna", "Barishal", "Rangpur", "Mymensingh"]

PERSONAS = {
    "Beach Baddie": ["beach", "island"],
    "Cloud Chaser": ["hill"],
    "Heritage Nerd": ["heritage"],
    "Jungle Junkie": ["forest", "wetland"],
    "Waterfall Hunter": ["waterfall"],
    "Chai & Chill": ["tea-garden"],
    "Street Food Explorer": ["urban"],
    "Off-Grid Wanderer": ["island", "wetland"],
}

BUDGETS = ["low", "medium", "high"]


def generate_destinations_csv():
    path = os.path.join(OUT_DIR, "bd_destinations.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "destination_id", "name", "division", "category", "vibe_tags",
            "budget_level", "best_season", "avg_cost_bdt_per_day",
            "instagrammability", "latitude", "longitude", "description"
        ])
        for i, d in enumerate(DESTINATIONS):
            name, division, category, tags, budget, season, cost, insta, lat, lon, desc = d
            writer.writerow([i, name, division, category, tags, budget, season, cost, insta, lat, lon, desc])
    return len(DESTINATIONS)


def generate_users_csv(n=120):
    path = os.path.join(OUT_DIR, "bd_users.csv")
    users = []
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "user_id", "name", "age", "home_city", "persona",
            "preferred_categories", "preferred_budget"
        ])
        for i in range(n):
            name = random.choice(FIRST_NAMES)
            age = random.randint(18, 27)
            city = random.choice(CITIES)
            persona = random.choice(list(PERSONAS.keys()))
            preferred_categories = "|".join(PERSONAS[persona])
            budget = random.choice(BUDGETS)
            writer.writerow([i, name, age, city, persona, preferred_categories, budget])
            users.append({"user_id": i, "persona": persona, "preferred_categories": PERSONAS[persona], "preferred_budget": budget})
    return users


def generate_ratings_csv(users, n_destinations, n_ratings=3000):
    path = os.path.join(OUT_DIR, "bd_ratings.csv")
    seasons = ["winter", "summer", "monsoon", "any"]
    seen = set()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "destination_id", "rating", "visited_season"])
        count = 0
        attempts = 0
        while count < n_ratings and attempts < n_ratings * 5:
            attempts += 1
            user = random.choice(users)
            dest_id = random.randint(0, n_destinations - 1)
            dest = DESTINATIONS[dest_id]
            key = (user["user_id"], dest_id)
            if key in seen:
                continue
            seen.add(key)

            base = 3.0
            if dest[2] in user["preferred_categories"]:
                base += 1.3
            if dest[5] == user["preferred_budget"]:
                base += 0.4
            rating = base + random.gauss(0, 0.8)
            rating = max(1, min(5, round(rating)))

            writer.writerow([user["user_id"], dest_id, int(rating), random.choice(seasons)])
            count += 1
    return count


if __name__ == "__main__":
    n_dest = generate_destinations_csv()
    users = generate_users_csv(n=120)
    n_ratings = generate_ratings_csv(users, n_dest, n_ratings=3000)
    print(f"Generated {n_dest} destinations, {len(users)} users, {n_ratings} ratings")
    print(f"Saved to: {os.path.abspath(OUT_DIR)}")
