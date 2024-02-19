# Copyright 2017  <https://incore.co/team/KolushovAlexandr>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import incore
from incore.tests.common import TransactionCase
# from incore.addons.point_of_sale.tests.common import TestPointOfSaleCommon


@incore.tests.common.at_install(False)
@incore.tests.common.post_install(True)
class TestPoSSessionState(TransactionCase):

    def test_current_session_state(self):

        self.pos_config = self.env.ref('point_of_sale.pos_config_main')

        # I click on create a new session button
        self.pos_config.open_session_cb()
        opened_session_pos = self.pos_config.id

        # Check that this session state is opened
        self.assertEqual(
            self.pos_config.current_session_state, 'opened')

        # _search_current_session_state function check
        poses_with_opened_sessions = self.env['pos.config'].search([('current_session_state', '=', 'opened')])
        poses_with_not_opened_sessions = self.env['pos.config'].search([('current_session_state', '!=', 'opened')])
        third_case = self.env['pos.config'].search([('current_session_state', '>', 'opened')])
        # Checking next cases: operator = '=', operator = '!=' and contradictory case
        self.assertIn(
            opened_session_pos, poses_with_opened_sessions.ids)
        self.assertNotIn(
            opened_session_pos, poses_with_not_opened_sessions.ids)
        self.assertEqual(
            len(third_case), 0)
