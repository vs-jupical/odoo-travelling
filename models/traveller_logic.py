from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Traveller(models.Model):

    _name = 'traveller.data'
    _description = "Traveller"
    _rec_name = 'traveller_name'


    @api.constrains('traveller_name','traveller_surname')
    def _check_values(self):
        for rec in self:
            if rec.traveller_name == rec.traveller_surname:
                raise ValidationError("Traveller name and Traveller surname must be not be same")
    

    traveller_name = fields.Char('Name')
    traveller_surname = fields.Char('Surname')
    travelling_date = fields.Date("Travelling Date")
    travelling_end_date = fields.Date("Travelling End Date")
    travelling_status = fields.Selection([
        ('active', 'Active'),
        ('non_active', 'Non Active')
    ], string="Travel Status", compute='_compute_travel_status')
    traveller_id = fields.Many2one("travelling.data", string="Travelling")
    journey_mode = fields.Char('Journey Mode')
    group_members = fields.Integer('Group Members')
    traveller_image = fields.Binary('Your Image')
    pasthistory_ids = fields.Many2many('travelling.data', 'travel_traveller_relation', 'travel_station', 'traveller_name', string='Your Past Travel History')
    travelling_station_mobile = fields.Char(related= 'traveller_id.mobile', store = True, string="travelling station mobile")


    @api.model
    def print_report(self, records):
        return self.env.ref('travelling.report_traveller_card').report_action(records)
    

    def _compute_travel_status(self):
        for record in self:
            if record.travelling_date and record.travelling_end_date:
                current_date = fields.Date.today()
                if record.travelling_date <= current_date <= record.travelling_end_date:
                    record.travelling_status = 'active'
                else:
                    record.travelling_status = 'non_active'
            else:
                record.travelling_status = False

    def unlink(self):
        if self.travelling_status == 'active':
            raise ValidationError(_('You cant delete this record because it is under travelling'))
        return super(Traveller, self).unlink()