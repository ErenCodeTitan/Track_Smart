from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_shipments():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "shipment_data.json")
    with open(file_path) as f:
        return json.load(f)

@app.route("/")
def dashboard():
    shipments = load_shipments()
    return render_template("dashboard.html", shipments=shipments)

@app.route("/map/<shipment_id>")
def map_view(shipment_id):
    shipments = load_shipments()
    shipment = next((s for s in shipments if s["id"] == shipment_id), None)
    if shipment:
        return render_template("map.html", shipment=shipment)
    else:
        return f"Shipment {shipment_id} not found.", 404

@app.route("/api/shipments")
def api_shipments():
    shipments = load_shipments()
    return jsonify(shipments)

@app.route("/new")
def new_shipment():
    return render_template("new_shipment.html")

@app.route("/create", methods=["POST"])
def create_shipment():
    shipments = load_shipments()

    new_id = request.form.get("id")
    from_city = request.form.get("from")
    to_city = request.form.get("to")
    start_lat = float(request.form.get("start_lat"))
    start_lng = float(request.form.get("start_lng"))
    dest_lat = float(request.form.get("dest_lat"))
    dest_lng = float(request.form.get("dest_lng"))

    new_shipment = {
        "id": new_id,
        "from": from_city,
        "to": to_city,
        "current_lat": start_lat,
        "current_lng": start_lng,
        "destination_lat": dest_lat,
        "destination_lng": dest_lng,
        "distance_km": 0,
        "eta_minutes": 0,
        "status": "Created"
    }

    shipments.append(new_shipment)

    with open("shipment_data.json", "w") as f:
        json.dump(shipments, f, indent=2)

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
