from incore import models

class ThemeinCore(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_incore_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
