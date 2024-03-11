from odoo import models, fields


class Traveller_tag(models.Model):
    _name = "traveller_tag.data"
    _description = "Traveller tag"
    _rec_name = 'agency_name'

    agency_name = fields.Char(string="Agency Name")
    active = fields.Boolean(string="Active", default=True)
    color = fields.Char(string="Color")



class Hr_data(models.Model):

    _inherit = "hr.employee"

    hr_travel_station = fields.Char("HR Travel Destination")