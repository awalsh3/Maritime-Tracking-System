import reflex as rx
import reflex_enterprise as rxe
from app.components import dashboard


def index() -> rx.Component:
    """The main page of the maritime tracking application."""
    return rx.el.main(
        rx.el.div(
            rx.el.header(
                rx.el.div(
                    "Inventories Tab",
                    class_name="border border-gray-200 rounded-lg px-4 py-2 text-sm font-medium text-gray-700 bg-white shadow-sm",
                ),
                class_name="flex items-center justify-center h-16 w-full",
            ),
            rx.el.div(
                rx.el.div(
                    "TIMELINE",
                    class_name="border border-gray-200 rounded-lg px-4 py-2 text-sm font-medium text-gray-700 bg-white shadow-sm w-full text-center mb-4",
                ),
                rx.el.div(
                    rx.el.div(dashboard.map_component(), class_name="lg:col-span-5"),
                    rx.el.div(dashboard.summary_tables(), class_name="lg:col-span-3"),
                    rx.el.div(
                        dashboard.filter_panel(),
                        dashboard.analytics_graphs(),
                        class_name="lg:col-span-4 flex flex-col gap-4",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-12 gap-6 w-full",
                ),
                dashboard.sequence_table(),
                class_name="w-full max-w-[1600px] mx-auto p-4 sm:p-6",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
    ],
)
app.add_page(index)