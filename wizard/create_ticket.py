from odoo import api, fields, models    

class CreateTicketWizard(models.TransientModel):
    _name = "create.ticket.wizard"
    _description = "Create Ticket Wizard"

    traveller_name_ticket = fields.Char(string="Name", required = True)
    traveller_id = fields.Many2one("travelling.data", string="Travelling")
    date_from = fields.Date(string = "Date From")
    date_to = fields.Date(string = "Date To")

    def action_print_ticket(self):
        data = {
            'form': self.read()[0],
        }
        return self.env.ref('travelling.action_create_ticket').report_action(self, data=data)