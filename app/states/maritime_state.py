import reflex as rx
import reflex_enterprise as rxe
from typing import TypedDict, Literal
from reflex_enterprise.components.map.types import LatLng, latlng
import datetime


class Vessel(TypedDict):
    """Data model for a single vessel."""

    id: str
    name: str
    type: str
    segment: str
    mmsi: str
    sizeband: str
    lat: float
    lng: float
    status: str
    origin_port: str
    destination_port: str
    voyage_duration_days: int
    distance_travelled_nm: int
    fuel_consumption_mt: int


class Event(TypedDict):
    """Data model for a vessel event."""

    id: str
    vessel_id: str
    timestamp: str
    event_type: Literal["Departure", "Arrival", "In Transit", "At Anchor"]
    location: str
    vessel_name: str


class MaritimeState(rx.State):
    """The state for the maritime tracking application."""

    events: list[Event] = [
        {
            "id": "event_1",
            "vessel_id": "vessel_1",
            "timestamp": "2023-10-26T10:00:00Z",
            "event_type": "Departure",
            "location": "Port of London",
            "vessel_name": "Container Ship Alpha",
        },
        {
            "id": "event_2",
            "vessel_id": "vessel_2",
            "timestamp": "2023-10-27T12:00:00Z",
            "event_type": "Arrival",
            "location": "Port of Rotterdam",
            "vessel_name": "Tanker Beta",
        },
        {
            "id": "event_3",
            "vessel_id": "vessel_3",
            "timestamp": "2023-10-28T14:30:00Z",
            "event_type": "In Transit",
            "location": "Mid-Atlantic",
            "vessel_name": "Bulk Carrier Gamma",
        },
        {
            "id": "event_4",
            "vessel_id": "vessel_4",
            "timestamp": "2023-10-29T08:00:00Z",
            "event_type": "At Anchor",
            "location": "Tokyo Bay",
            "vessel_name": "Ferry Delta",
        },
        {
            "id": "event_5",
            "vessel_id": "vessel_5",
            "timestamp": "2023-10-30T18:00:00Z",
            "event_type": "Departure",
            "location": "Port of Sydney",
            "vessel_name": "Cargo Ship Echo",
        },
        {
            "id": "event_6",
            "vessel_id": "vessel_1",
            "timestamp": "2023-11-05T22:00:00Z",
            "event_type": "Arrival",
            "location": "Port of New York",
            "vessel_name": "Container Ship Alpha",
        },
    ]
    center: LatLng = latlng(lat=30.0, lng=0.0)
    zoom: float = 2.5
    selected_segment: str = ""
    selected_type: str = ""
    selected_mmsi: str = ""
    selected_sizeband: str = ""
    selected_origin_port: str = ""
    selected_destination_port: str = ""
    vessels: list[Vessel] = [
        {
            "id": "vessel_1",
            "name": "Container Ship Alpha",
            "type": "Container",
            "segment": "Deep Sea",
            "mmsi": "123456789",
            "sizeband": "Large",
            "lat": 51.5074,
            "lng": -0.1278,
            "status": "In Transit",
            "origin_port": "Port of London",
            "destination_port": "Port of New York",
            "voyage_duration_days": 10,
            "distance_travelled_nm": 3440,
            "fuel_consumption_mt": 500,
        },
        {
            "id": "vessel_2",
            "name": "Tanker Beta",
            "type": "Tanker",
            "segment": "Coastal",
            "mmsi": "987654321",
            "sizeband": "Medium",
            "lat": 48.8566,
            "lng": 2.3522,
            "status": "At Port",
            "origin_port": "Port of Le Havre",
            "destination_port": "Port of Rotterdam",
            "voyage_duration_days": 1,
            "distance_travelled_nm": 160,
            "fuel_consumption_mt": 20,
        },
        {
            "id": "vessel_3",
            "name": "Bulk Carrier Gamma",
            "type": "Bulk Carrier",
            "segment": "Deep Sea",
            "mmsi": "555666777",
            "sizeband": "Large",
            "lat": 40.7128,
            "lng": -74.006,
            "status": "In Transit",
            "origin_port": "Port of New York",
            "destination_port": "Port of Shanghai",
            "voyage_duration_days": 25,
            "distance_travelled_nm": 10500,
            "fuel_consumption_mt": 1200,
        },
        {
            "id": "vessel_4",
            "name": "Ferry Delta",
            "type": "Ferry",
            "segment": "Coastal",
            "mmsi": "111222333",
            "sizeband": "Small",
            "lat": 35.6762,
            "lng": 139.6503,
            "status": "At Port",
            "origin_port": "Port of Tokyo",
            "destination_port": "Port of Osaka",
            "voyage_duration_days": 1,
            "distance_travelled_nm": 300,
            "fuel_consumption_mt": 50,
        },
        {
            "id": "vessel_5",
            "name": "Cargo Ship Echo",
            "type": "Cargo",
            "segment": "Deep Sea",
            "mmsi": "444555666",
            "sizeband": "Medium",
            "lat": -33.8688,
            "lng": 151.2093,
            "status": "In Transit",
            "origin_port": "Port of Sydney",
            "destination_port": "Port of Singapore",
            "voyage_duration_days": 15,
            "distance_travelled_nm": 3900,
            "fuel_consumption_mt": 800,
        },
    ]

    @rx.event
    def handle_zoom(self, event: dict):
        self.zoom = round(event["target"]["zoom"], 4)

    @rx.event
    def reset_filters(self):
        self.selected_segment = ""
        self.selected_type = ""
        self.selected_mmsi = ""
        self.selected_sizeband = ""
        self.selected_origin_port = ""
        self.selected_destination_port = ""

    @rx.var
    def filtered_vessels(self) -> list[Vessel]:
        """Get the vessels that match the current filters."""
        return [
            vessel
            for vessel in self.vessels
            if (not self.selected_segment or vessel["segment"] == self.selected_segment)
            and (not self.selected_type or vessel["type"] == self.selected_type)
            and (not self.selected_mmsi or vessel["mmsi"] == self.selected_mmsi)
            and (
                not self.selected_sizeband
                or vessel["sizeband"] == self.selected_sizeband
            )
            and (
                not self.selected_origin_port
                or vessel["origin_port"] == self.selected_origin_port
            )
            and (
                not self.selected_destination_port
                or vessel["destination_port"] == self.selected_destination_port
            )
        ]

    @rx.var
    def unique_segments(self) -> list[str]:
        return sorted(list(set((v["segment"] for v in self.vessels))))

    @rx.var
    def unique_vessel_types(self) -> list[str]:
        return sorted(list(set((v["type"] for v in self.vessels))))

    @rx.var
    def unique_mmsi(self) -> list[str]:
        return sorted(list(set((v["mmsi"] for v in self.vessels))))

    @rx.var
    def unique_sizebands(self) -> list[str]:
        return sorted(list(set((v["sizeband"] for v in self.vessels))))

    @rx.var
    def unique_origin_ports(self) -> list[str]:
        return sorted(list(set((v["origin_port"] for v in self.vessels))))

    @rx.var
    def unique_destination_ports(self) -> list[str]:
        return sorted(list(set((v["destination_port"] for v in self.vessels))))

    @rx.var
    def voyage_stats(self) -> dict[str, int | float]:
        """Calculate statistics for the filtered vessels."""
        if not self.filtered_vessels:
            return {
                "total_voyages": 0,
                "avg_duration_days": 0,
                "total_distance_nm": 0,
                "total_fuel_mt": 0,
            }
        total_voyages = len(self.filtered_vessels)
        total_duration = sum((v["voyage_duration_days"] for v in self.filtered_vessels))
        avg_duration = round(total_duration / total_voyages, 1)
        total_distance = sum(
            (v["distance_travelled_nm"] for v in self.filtered_vessels)
        )
        total_fuel = sum((v["fuel_consumption_mt"] for v in self.filtered_vessels))
        return {
            "total_voyages": total_voyages,
            "avg_duration_days": avg_duration,
            "total_distance_nm": total_distance,
            "total_fuel_mt": total_fuel,
        }

    @rx.var
    def recent_events(self) -> list[Event]:
        """Get the most recent events for the filtered vessels."""
        filtered_vessel_ids = {v["id"] for v in self.filtered_vessels}
        filtered = [e for e in self.events if e["vessel_id"] in filtered_vessel_ids]
        return sorted(filtered, key=lambda e: e["timestamp"], reverse=True)

    @rx.event
    def fly_to_vessel(self, vessel: Vessel) -> rx.event.EventSpec:
        map_api = rxe.map.api("maritime_map")
        return map_api.fly_to(latlng(lat=vessel["lat"], lng=vessel["lng"]), 10.0)