
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number

import logging
_logger = logging.getLogger(__name__)



class ResCompanyOcr(models.Model):
    _inherit = 'res.company'


    server_port = fields.Char(
        string='Port',
    )
    server_url = fields.Char(
        string='Api Url'
    )