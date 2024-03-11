from odoo import fields, models

class Travel_Country(models.Model):
    _name="travelling_country.data"
    _description = "Travelling Country"
    _rec_name = 'country_name'

    country_name = fields.Char("Country Name")
    country_image = fields.Binary('Travelling Country Image')
    travelling_state_ids = fields.One2many('travelling_state.data','travelling_country_id')
