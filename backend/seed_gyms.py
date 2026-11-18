"""Seed real gyms for local testing. Safe to run more than once.

Run from the backend folder:  python seed_gyms.py

Before running: fill in latitude/longitude for each gym (in Google Maps, right-click the gym's pin
and click the numbers at the top of the menu to copy them). Gyms without coordinates are skipped.
Equipment: leave the list empty if you don't know it. After visiting a gym, add real equipment
through the app's equipment form on the gym page. Format: (name, availability, condition)
  availability: available / unavailable / unconfirmed     condition: good / fair / worn / broken
"""
from app.database import SessionLocal
from app.models import Equipment, Gym

# (name, address, latitude, longitude, equipment). Addresses came from public listings: confirm on the gym's site.
GYMS = [
    ("Planet Fitness San Jose (Princeton Plaza)", "1375 Blossom Hill Rd, San Jose, CA 95118",
     37.244897, -121.889716, [
         ("Smith Machine", "available", "good"),
         ("Treadmill", "available", "good"),
         ("Elliptical", "available", "good"),
         ("Cable Tower", "available", "good"),
         ("Dumbbells", "available", "good"),
         ("30-Minute Circuit Machines", "available", "good"),
     ]),
    ("Planet Fitness San Jose (S White Rd)", "3251 S White Rd, San Jose, CA 95148",
     37.315003, -121.793718, [
         ("Smith Machine", "available", "good"),
         ("Treadmill", "available", "good"),
         ("Elliptical", "available", "good"),
         ("Cable Tower", "available", "good"),
         ("Dumbbells", "available", "good"),
     ]),
    ("Planet Fitness San Jose (Monterey Rd)", "1462 Monterey Rd, San Jose, CA 95110",
     37.315851, -121.870804, [
         ("Smith Machine", "available", "good"),
         ("Treadmill", "available", "good"),
         ("Elliptical", "available", "good"),
         ("Free Weights & Benches", "available", "good"),
         ("30-Minute Circuit Machines", "available", "good"),
     ]),
    ("Planet Fitness San Jose (E Capitol Expy)", "1035 E Capitol Expy #20, San Jose, CA 95121",
     37.300980, -121.823410, [
         ("Smith Machine", "available", "good"),
         ("Treadmill", "available", "good"),
         ("Cable Tower", "available", "good"),
         ("Dumbbells", "available", "good"),
         ("30-Minute Circuit Machines", "available", "good"),
     ]),
    ("Planet Fitness San Jose (Saratoga Ave)", "1328 Saratoga Ave, San Jose, CA 95129",
     37.311300, -121.999500, [
         ("Smith Machine", "available", "good"),
         ("Treadmill", "available", "good"),
         ("Elliptical", "available", "good"),
         ("Cable Tower", "available", "good"),
         ("Free Weights", "available", "good"),
     ]),
    ("Planet Fitness Milpitas (Ranch Dr)", "158 Ranch Dr, Milpitas, CA 95035",
     37.428150, -121.922180, [
         ("Smith Machine", "available", "good"),
         ("Treadmill", "available", "good"),
         ("Elliptical", "available", "good"),
         ("Cable Tower", "available", "good"),
         ("Dumbbells", "available", "good"),
     ]),
    ("Vim + Vigor Fitness", "3055 Meridian Ave, San Jose, CA 95124",
     37.269766, -121.906833, [
         ("Squat Rack", "available", "good"),
         ("Bumper Plates", "available", "good"),
         ("Free Weights", "available", "good"),
         ("Indoor Astro-Turf", "available", "good"),
         ("Kettlebells", "available", "good"),
         ("TRX Suspension Trainer", "available", "good"),
         ("Cardio Machines", "available", "good"),
     ]),
    ("WARCAT Strength", "2532 Seaboard Ave, San Jose, CA 95131",
     37.384910, -121.902460, [
         ("Power Rack", "available", "good"),
         ("Combo Rack", "available", "good"),
         ("Deadlift Platform", "available", "good"),
         ("Calibrated Plates", "available", "good"),
         ("Cable Machine", "available", "good"),
     ]),
    ("Gold's Gym Milpitas", "301 Jacklin Rd, Milpitas, CA 95035",
     37.450360, -121.916588, [
         ("Squat Rack", "available", "good"),
         ("Glute Machines", "available", "good"),
         ("Leg Press", "available", "good"),
         ("Free Weights", "available", "good"),
         ("Kettlebells", "available", "good"),
         ("Cardio Machines", "available", "good"),
     ]),
    ("Forma Gym", "5434 Thornwood Dr, San Jose, CA 95123",
     37.254751, -121.860336, [
         ("Outdoor Weight Area", "available", "good"),
         ("Outdoor Turf", "available", "good"),
         ("Heavy Punching Bag", "available", "good"),
         ("Spin Bike", "available", "good"),
         ("Pilates Reformer", "unconfirmed", "good"),
         ("Heated Lap Pool", "available", "good"),
     ]),
    ("Villa Sport Athletic Club", "1167 N Capitol Ave, San Jose, CA 95132",
     37.386389, -121.863333, [
         ("Free Weights", "available", "good"),
         ("Cardio Machines", "available", "good"),
         ("Spin Bike", "available", "good"),
         ("Basketball Court", "available", "good"),
         ("Indoor & Outdoor Lap Pools", "available", "good"),
     ]),
    ("24 Hour Fitness (McKee Rd)", "2323 McKee Rd, San Jose, CA 95116",
     37.366630, -121.850869, [
         ("Functional Turf", "available", "good"),
         ("Free Weights", "available", "good"),
         ("Cardio Machines", "available", "good"),
         ("Basketball Court", "available", "good"),
         ("Swimming Pool", "available", "good"),
     ]),
    ("City Sports Club (Brokaw Rd)", "1045 E Brokaw Rd, San Jose, CA 95131",
     37.382979, -121.897868, [
         ("Squat Rack", "available", "good"),
         ("Free Weights", "available", "good"),
         ("Cardio Machines", "available", "good"),
         ("Spin Bike", "available", "good"),
         ("Basketball & Racquetball Courts", "available", "good"),
         ("Lap Pool", "available", "good"),
     ]),
    ("Hyper Strength and Conditioning", "385 E Taylor St Unit 2B, San Jose, CA 95112",
     37.354432, -121.893205, [
         ("Powerlifting Rack", "available", "good"),
         ("Barbells & Bumper Plates", "available", "good"),
         ("Concept2 Erg", "available", "good"),
         ("Conditioning Turf", "available", "good"),
     ]),
    ("YBX Fitness", "452 S 1st St, San Jose, CA 95113",
     37.329680, -121.885580, [
         ("Heavy Boxing Bag", "available", "good"),
         ("Free Weights", "available", "good"),
         ("Hyrox Conditioning Stations", "available", "good"),
         ("Yoga Mats", "available", "good"),
     ]),
    ("Grit & Glory Boxing Fitness", "394 Barack Obama Blvd, San Jose, CA 95126",
     37.323650, -121.899190, [
         ("Heavy Boxing Bag", "available", "good"),
         ("Speed Bag", "unconfirmed", "good"),
         ("Free Weights", "available", "good"),
         ("Conditioning Equipment", "available", "good"),
     ]),
]


def main():
    db = SessionLocal()
    try:
        added_gyms = added_equipment = 0
        for name, address, lat, lng, equipment in GYMS:
            if lat is None or lng is None:
                print(f"Skipped (add latitude/longitude first): {name}")
                continue
            gym = db.query(Gym).filter(Gym.name == name).first()
            if gym is None:
                gym = Gym(name=name, address=address, latitude=lat, longitude=lng)
                db.add(gym)
                db.flush()
                added_gyms += 1
            for item, availability, condition in equipment:
                if db.query(Equipment).filter(Equipment.gym_id == gym.id, Equipment.name == item).first() is None:
                    db.add(Equipment(gym_id=gym.id, name=item, availability=availability, condition=condition))
                    added_equipment += 1
        db.commit()
        print(f"Added {added_gyms} gyms and {added_equipment} equipment rows")
    finally:
        db.close()


if __name__ == "__main__":
    main()
