# Copyright 2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
# License MIT (https://opensource.org/licenses/MIT).

import incore
from incore.http import request

try:
    from incore.addons.bus.controllers.main import BusController
except ImportError:
    BusController = object


class Controller(BusController):
    @incore.http.route("/pos_order_test/update", type="json", auth="public")
    def order_test_update(self, message):
        channel_name = "pos.order_test"
        res = request.env["pos.config"]._send_to_channel(channel_name, message)
        return res
