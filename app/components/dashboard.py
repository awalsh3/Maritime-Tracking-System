import reflex as rx
import reflex_enterprise as rxe
from app.states.maritime_state import MaritimeState, Vessel
from reflex_enterprise.components.map.types import latlng


def card(
    title: str, content: rx.Component | None = None, class_name: str = ""
) -> rx.Component:
    """A reusable card component with a title."""
    return rx.el.div(
        rx.el.p(title, class_name="font-semibold text-sm text-gray-700"),
        rx.el.div(content if content else rx.el.div(), class_name="mt-2"),
        class_name=f"border border-gray-200 rounded-lg p-4 bg-white shadow-sm {class_name}",
    )


def vessel_marker(vessel: Vessel) -> rx.Component:
    return rxe.map.marker(
        rxe.map.popup(
            rx.el.div(
                rx.el.p(vessel["name"], class_name="font-bold"),
                rx.el.p(f"Type: {vessel['type']}"),
                rx.el.p(f"Status: {vessel['status']}"),
            )
        ),
        rxe.map.tooltip(vessel["name"]),
        position=latlng(lat=vessel["lat"], lng=vessel["lng"]),
    )


def map_component() -> rx.Component:
    """The interactive map component for displaying vessels."""
    map_api = rxe.map.api("maritime_map")
    return rxe.map(
        rxe.map.tile_layer(
            url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        ),
        rx.foreach(MaritimeState.filtered_vessels, vessel_marker),
        rxe.map.zoom_control(position="bottomright"),
        id="maritime_map",
        center=MaritimeState.center,
        zoom=MaritimeState.zoom,
        on_zoom=MaritimeState.handle_zoom,
        class_name="border border-gray-200 rounded-lg w-full h-full min-h-[600px] lg:min-h-0 z-0",
    )


def summary_tables() -> rx.Component:
    """Summary tables for voyage stats and vessel characteristics."""

    def voyage_stats_table() -> rx.Component:
        return rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Metric",
                        class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                    ),
                    rx.el.th(
                        "Value",
                        class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase",
                    ),
                )
            ),
            rx.el.tbody(
                rx.el.tr(
                    rx.el.td(
                        "Total Voyages",
                        class_name="border-t px-4 py-2 text-sm text-gray-700",
                    ),
                    rx.el.td(
                        MaritimeState.voyage_stats["total_voyages"],
                        class_name="border-t px-4 py-2 text-sm font-medium text-gray-900",
                    ),
                ),
                rx.el.tr(
                    rx.el.td(
                        "Avg Duration (days)",
                        class_name="border-t px-4 py-2 text-sm text-gray-700",
                    ),
                    rx.el.td(
                        MaritimeState.voyage_stats["avg_duration_days"],
                        class_name="border-t px-4 py-2 text-sm font-medium text-gray-900",
                    ),
                ),
                rx.el.tr(
                    rx.el.td(
                        "Total Distance (nm)",
                        class_name="border-t px-4 py-2 text-sm text-gray-700",
                    ),
                    rx.el.td(
                        MaritimeState.voyage_stats["total_distance_nm"],
                        class_name="border-t px-4 py-2 text-sm font-medium text-gray-900",
                    ),
                ),
                rx.el.tr(
                    rx.el.td(
                        "Total Fuel (mt)",
                        class_name="border-t px-4 py-2 text-sm text-gray-700",
                    ),
                    rx.el.td(
                        MaritimeState.voyage_stats["total_fuel_mt"],
                        class_name="border-t px-4 py-2 text-sm font-medium text-gray-900",
                    ),
                ),
            ),
            class_name="w-full",
        )

    def vessel_char_table() -> rx.Component:
        header = ["Vessel", "Type", "Segment", "MMSI", "Sizeband", "Status"]

        def row(vessel: Vessel):
            return rx.el.tr(
                rx.el.td(
                    vessel["name"],
                    class_name="border-t px-4 py-2 text-sm text-gray-700 whitespace-nowrap",
                ),
                rx.el.td(
                    vessel["type"],
                    class_name="border-t px-4 py-2 text-sm text-gray-700 whitespace-nowrap",
                ),
                rx.el.td(
                    vessel["segment"],
                    class_name="border-t px-4 py-2 text-sm text-gray-700 whitespace-nowrap",
                ),
                rx.el.td(
                    vessel["mmsi"],
                    class_name="border-t px-4 py-2 text-sm text-gray-700 whitespace-nowrap",
                ),
                rx.el.td(
                    vessel["sizeband"],
                    class_name="border-t px-4 py-2 text-sm text-gray-700 whitespace-nowrap",
                ),
                rx.el.td(
                    vessel["status"],
                    class_name="border-t px-4 py-2 text-sm text-gray-700 whitespace-nowrap",
                ),
                on_click=MaritimeState.fly_to_vessel(vessel),
                class_name="cursor-pointer hover:bg-gray-50",
            )

        return rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            header,
                            lambda h: rx.el.th(
                                h,
                                class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase bg-gray-50",
                            ),
                        )
                    )
                ),
                rx.el.tbody(rx.foreach(MaritimeState.filtered_vessels, row)),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto border border-gray-200 rounded-lg",
        )

    return rx.el.div(
        card("Voyages stats Summary table", voyage_stats_table()),
        card("Vessel Characteristic Summary", vessel_char_table()),
        class_name="flex flex-col gap-4 w-full",
    )


def select_filter(
    label: str,
    options: rx.Var[list[str]],
    value: rx.Var[str],
    on_change: rx.event.EventSpec,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-xs font-medium text-gray-600"),
        rx.el.select(
            rx.el.option("All", value=""),
            rx.foreach(options, lambda option: rx.el.option(option, value=option)),
            value=value,
            on_change=on_change,
            class_name="w-full mt-1 p-2 border border-gray-300 rounded-lg bg-white text-sm",
        ),
        class_name="w-full",
    )


def filter_panel() -> rx.Component:
    """Filter controls for vessels and routes."""
    return rx.el.div(
        rx.el.button(
            "Reset Filters",
            on_click=MaritimeState.reset_filters,
            class_name="w-full bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg border border-gray-300 transition-colors",
        ),
        card(
            "Vessels Filters",
            rx.el.div(
                select_filter(
                    "Segment",
                    MaritimeState.unique_segments,
                    MaritimeState.selected_segment,
                    MaritimeState.set_selected_segment,
                ),
                select_filter(
                    "Vessel type",
                    MaritimeState.unique_vessel_types,
                    MaritimeState.selected_type,
                    MaritimeState.set_selected_type,
                ),
                select_filter(
                    "MMSI",
                    MaritimeState.unique_mmsi,
                    MaritimeState.selected_mmsi,
                    MaritimeState.set_selected_mmsi,
                ),
                select_filter(
                    "Sizeband",
                    MaritimeState.unique_sizebands,
                    MaritimeState.selected_sizeband,
                    MaritimeState.set_selected_sizeband,
                ),
                class_name="space-y-3",
            ),
            class_name="mt-4",
        ),
        card(
            "Route Filter",
            rx.el.div(
                select_filter(
                    "Origin Port",
                    MaritimeState.unique_origin_ports,
                    MaritimeState.selected_origin_port,
                    MaritimeState.set_selected_origin_port,
                ),
                select_filter(
                    "Destination Port",
                    MaritimeState.unique_destination_ports,
                    MaritimeState.selected_destination_port,
                    MaritimeState.set_selected_destination_port,
                ),
                class_name="space-y-3",
            ),
            class_name="mt-4",
        ),
        class_name="w-full",
    )


def analytics_graphs() -> rx.Component:
    """Placeholder for analytics graphs."""
    return card(
        "Analytic graphs",
        rx.el.div(
            card("Stacked Bar chart for totals...", class_name="bg-gray-50"),
            card("Emissions by Port", class_name="bg-gray-50"),
            card("tbd", class_name="bg-gray-50"),
            card("Emissions by Route", class_name="bg-gray-50"),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2",
        ),
        class_name="w-full mt-4",
    )


def sequence_table() -> rx.Component:
    """A table showing the sequence of vessel events."""
    header = ["Timestamp", "Vessel", "Event Type", "Location"]

    def row(event: dict) -> rx.Component:
        return rx.el.tr(
            rx.el.td(
                event["timestamp"],
                class_name="border-t px-4 py-2 text-sm text-gray-700",
            ),
            rx.el.td(
                event["vessel_name"],
                class_name="border-t px-4 py-2 text-sm text-gray-700",
            ),
            rx.el.td(
                event["event_type"],
                class_name="border-t px-4 py-2 text-sm text-gray-700",
            ),
            rx.el.td(
                event["location"], class_name="border-t px-4 py-2 text-sm text-gray-700"
            ),
        )

    return rx.el.div(
        rx.el.p("Sequence of events table", class_name="font-semibold text-gray-800"),
        rx.el.p(
            "(time ordered showing the most recent calling/journey)",
            class_name="text-sm text-gray-500 mt-1 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.foreach(
                            header,
                            lambda h: rx.el.th(
                                h,
                                class_name="px-4 py-2 text-left text-xs font-semibold text-gray-600 uppercase bg-gray-50",
                            ),
                        )
                    )
                ),
                rx.el.tbody(rx.foreach(MaritimeState.recent_events, row)),
                class_name="w-full",
            ),
            class_name="w-full overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm",
        ),
        class_name="w-full mt-6",
    )