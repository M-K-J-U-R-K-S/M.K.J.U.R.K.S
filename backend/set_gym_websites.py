"""Set each gym's website link. Safe to run more than once.

Run from the backend folder:  python set_gym_websites.py
Run this SQL in Supabase first (once):  alter table gyms add column if not exists website text;

Matches by (name, address) first so duplicate chain names (like "Planet Fitness") get their exact
location URL, then falls back to matching by name.
"""
from app.database import SessionLocal
from app.models import Gym

# Exact (name, address) matches for locations that share the same name in your CSV
WEBSITES_BY_NAME_AND_ADDRESS = {
    ("Planet Fitness", "1035 E Capitol Expy Ste 20, San Jose, CA 95121, USA"): "https://planetfitness.com",
    ("Planet Fitness", "1328 Saratoga Ave, San Jose, CA 95129, USA"): "https://www.planetfitness.com/gyms/san-jose-saratoga-ave-ca",
    ("Planet Fitness", "610 Hegenberger Rd, Oakland, CA 94621, USA"): "https://planetfitness.com",
    ("Planet Fitness", "3251 S White Rd, San Jose, CA 95148, USA"): "https://planetfitness.com",
    ("Planet Fitness", "4055 MacArthur Blvd, Oakland, CA 94619, USA"): "https://planetfitness.com",
    ("Planet Fitness", "1375 Blossom Hill Rd, San Jose, CA 95118, USA"): "https://www.planetfitness.com/gyms/san-jose-princeton-plaza-ca",
    ("Planet Fitness", "4349 San Pablo Ave, Emeryville, CA 94608, USA"): "https://planetfitness.com",
    ("Planet Fitness", "1697 Mt Diablo Blvd, Walnut Creek, CA 94596, USA"): "https://planetfitness.com",
    ("Planet Fitness", "1150 El Camino Real Unit 209, San Bruno, CA 94066, USA"): "https://planetfitness.com",
    ("Planet Fitness", "42 Springstowne Center, Vallejo, CA 94591, USA"): "https://www.planetfitness.com/gyms/vallejo-central-ca/",
    ("Planet Fitness", "3375 Port Chicago Hwy Ste 51, Concord, CA 94520, USA"): "https://www.planetfitness.com/gyms/concord-ca/",
    ("Planet Fitness", "900 Market St #301, Oakland, CA 94607, USA"): "https://planetfitness.com",
    ("Planet Fitness", "5140 Mowry Ave, Fremont, CA 94538, USA"): "https://planetfitness.com",
    ("Planet Fitness", "35630 Fremont Blvd, Fremont, CA 94536, USA"): "https://planetfitness.com",
    ("Planet Fitness", "214 B Southland Mall, Hayward, CA 94545, USA"): "https://www.planetfitness.com/gyms/hayward-ca/",
    ("Planet Fitness", "158 Ranch Dr, Milpitas, CA 95035, USA"): "https://planetfitness.com",
    ("Planet Fitness", "242 Walnut St, Redwood City, CA 94063, USA"): "https://www.planetfitness.com/gyms/redwood-city-ca/",
    ("Planet Fitness", "1462 Monterey Rd, San Jose, CA 95110, USA"): "https://planetfitness.com",
    ("Planet Fitness", "10715 MacArthur Blvd, Oakland, CA 94605, USA"): "https://planetfitness.com",
}

# Unique gym names
WEBSITES = {
    # Named Planet Fitness entries
    "Planet Fitness Milpitas (Ranch Dr)": "https://planetfitness.com",
    "Planet Fitness San Jose (E Capitol Expy)": "https://planetfitness.com",
    "Planet Fitness San Jose (Monterey Rd)": "https://planetfitness.com",
    "Planet Fitness San Jose (Princeton Plaza)": "https://www.planetfitness.com/gyms/san-jose-princeton-plaza-ca",
    "Planet Fitness San Jose (S White Rd)": "https://planetfitness.com",
    "Planet Fitness San Jose (Saratoga Ave)": "https://www.planetfitness.com/gyms/san-jose-saratoga-ave-ca",
    # Local & chain gyms from your CSV
    "24 Hour Fitness (McKee Rd)": "https://24hourfitness.com",
    "City Sports Club (Brokaw Rd)": "https://citysportsfitness.com",
    "Fitness 19": "https://fit19.com",
    "Forma Gym": "https://formagym.com",
    "Gold's Gym Milpitas": "https://goldsgym.com",
    "Grit & Glory Boxing Fitness": "https://gritgloryboxing.com",
    "Hyper Strength and Conditioning": "https://hscgym.com",
    "StretchLab Fremont": "https://stretchlab.com",
    "The Bar Method Fremont": "https://barmethod.com",
    "Villa Sport Athletic Club": "https://www.villasport.com/san-jose/",
    "Vim + Vigor Fitness": "https://vnvfit.com",
    "WARCAT Strength": "https://warcatfitness.com",
    "YBX Fitness": "https://ybxfitness.com",
    # Test entry in CSV (left blank)
    "Jason test": None,
    # Extra gyms from previous search results:
    "Crunch Fitness Winchester": "https://www.crunch.com/locations/winchester",
    "Crunch Fitness San Jose": "https://www.crunch.com/locations/san-jose",
    "Anytime Fitness San Jose (The Alameda)": "https://www.anytimefitness.com/locations/san-jose-california-5039/",
    "Anytime Fitness San Jose (Branham Ln)": "https://www.anytimefitness.com/locations/san-jose-california-4922/",
}


def main():
    db = SessionLocal()
    try:
        updated, skipped = 0, []

        # 1. Update duplicate-name locations using exact (name, address)
        for (name, address), url in WEBSITES_BY_NAME_AND_ADDRESS.items():
            if not url:
                continue
            gyms = db.query(Gym).filter(Gym.name == name, Gym.address == address).all()
            if not gyms:
                skipped.append(f"{name} ({address})")
            for gym in gyms:
                gym.website = url
                updated += 1

        # 2. Update unique-name gyms
        for name, url in WEBSITES.items():
            if not url:
                continue
            gyms = db.query(Gym).filter(Gym.name == name).all()
            if not gyms:
                skipped.append(name)
            for gym in gyms:
                gym.website = url
                updated += 1

        db.commit()
        print(f"Updated {updated} gyms")
        if skipped:
            print("Not in your database (ignored):", ", ".join(skipped))
        missing = [g.name for g in db.query(Gym).filter(Gym.website.is_(None)).order_by(Gym.name)]
        if missing:
            print("Still no website:", ", ".join(missing))
    finally:
        db.close()


if __name__ == "__main__":
    main()
