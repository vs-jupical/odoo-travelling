from odoo import fields, models

class Travel_State(models.Model):
    _name="travelling_state.data"
    _description = "Travelling States"
    _rec_name = 'state_name'

    travelling_country_id = fields.Many2one('travelling_country.data', string="Travelling Country")
    state_name = fields.Char("State Name")
    state_image = fields.Binary('Travelling State Image')
    travelling_station_ids = fields.One2many('travelling.data','travelling_state_id')