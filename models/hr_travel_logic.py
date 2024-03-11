from odoo import models, fields


class Hr_data(models.Model):

    _inherit = "hr.employee"

    hr_travel_station = fields.Char("HR Travel Destination")