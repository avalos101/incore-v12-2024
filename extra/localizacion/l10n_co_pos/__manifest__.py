# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Punto de venta adaptado a la legislación Colombiana",
    "category": "Point Of Sale",
    "author": "inCore",
    "version": "12.0.2.0.0",
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "views/pos_templates.xml",
        "views/pos_views.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
