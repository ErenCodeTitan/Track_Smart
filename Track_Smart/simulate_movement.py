import json
import time
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def move_towards(current, dest, step=0.1):
    lat, lng = current
    d_lat = dest[0] - lat
    d_lng = dest[1] - lng
    dist = math.hypot(d_lat, d_lng)
    if dist < step:
        return dest
    factor = step / dist
    new_lat = lat + d_lat * factor
    new_lng = lng + d_lng * factor
    return round(new_lat, 6), round(new_lng, 6)

while True:
    with open("shipment_data.json") as f:
        shipments = json.load(f)

    for s in shipments:
        current = (s["current_lat"], s["current_lng"])
        dest = (s["destination_lat"], s["destination_lng"])
        new_lat, new_lng = move_towards(current, dest)
        s["current_lat"] = new_lat
        s["current_lng"] = new_lng

        distance_km = haversine(new_lat, new_lng, dest[0], dest[1])
        s["distance_km"] = round(distance_km, 2)
        speed_kmh = 60
        eta_hours = distance_km / speed_kmh if speed_kmh > 0 else 0
        eta_minutes = round(eta_hours * 60)

        s["eta_minutes"] = eta_minutes

        if distance_km < 0.5:
            s["status"] = "Delivered"
        elif new_lat != s["destination_lat"] or new_lng != s["destination_lng"]:
            s["status"] = f"In Transit: {round(new_lat,4)}, {round(new_lng,4)}"
        else:
            s["status"] = "Departed"

    with open("shipment_data.json", "w") as f:
        json.dump(shipments, f, indent=2)

    time.sleep(5)
