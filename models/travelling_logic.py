from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class Travel(models.Model):
    _name="travelling.data"
    _description = "Travelling"
    _rec_name = 'name'
    _sql_constraints = [('key_uniq','unique(name)','Travel station name must be unique.')]

    travelling_state_id = fields.Many2one('travelling_state.data', string="Travelling State")
    name = fields.Char("Travel Station")
    mobile = fields.Char("Mobile")
    travel_distance = fields.Integer("Travel Distance")
    travel_date = fields.Date("Travel Date")
    travel_end_date = fields.Date("Travel End Date")
    travelling_station_image = fields.Binary('Travelling Station Image')
    good_place = fields.Selection([('type1', 'Yes'),('type2', 'No')])
    traveller_ids = fields.One2many('traveller.data','traveller_id')
    travel_description = fields.Html()
    your_query = fields.Text("Your Query")
    ticket = fields.Float("Ticket Price")
    traveller_count = fields.Integer(compute = 'get_traveller_count', store = True)
    history_count = fields.Integer(compute = 'get_history_count', store = True)
    days_difference = fields.Char(compute='difference_date', string="Days Difference")
    total_visitors = fields.Integer(compute='get_total_visitors', string="Total Visitors")
    travel_seq_id = fields.Char("Travel", copy=False)
    color_m2m = fields.Integer(string="Color")



    # traveller button count
    @api.depends('traveller_ids')
    def get_traveller_count(self):
        for rec in self:
            # print("self===",self)
            # self.traveller_count=5
            rec.traveller_count = len(rec.traveller_ids)


    # traveller button count action
    def action_view_traveller(self):
        traveller_ids=[]
        return{
            'type':'ir.actions.act_window',
            'view_mode':'tree',
            'res_model':'traveller.data',
            'target':'current',
            'domain':[('id','in',self.traveller_ids.ids)]
        }
    

    # total visitor counting 
    @api.depends('traveller_ids.group_members')
    def get_total_visitors(self):
        for rec in self:
            total = 0
            for line in rec.traveller_ids:
                total += line.group_members
            rec.total_visitors = total


    # days difference function
    def difference_date(self):
        for rec in self:
            if rec.travel_date:
                travel_date = fields.Date.from_string(rec.travel_date)
                today_date = datetime.now().date()
                
                difference = today_date - travel_date

                years_difference = difference.days // 365
                remaining_days = difference.days % 365
                months_difference = remaining_days // 30
                remaining_days %= 30
                weeks_difference = difference.days // 7
                days_difference = difference.days

                diff_str = ""
                if years_difference:
                    diff_str += f"{years_difference} year(s) "
                if months_difference:
                    diff_str += f"{months_difference} month(s) "
                if weeks_difference:
                    diff_str += f"{weeks_difference} week(s) "
                diff_str += f"{days_difference} day(s)"

                rec.days_difference = diff_str


    @api.onchange('mobile')
    def onchange_mobile(self):
        if self.mobile:
            mobile_len=len(self.mobile)
            if mobile_len != 10:
                raise ValidationError(_("You must have to add 10 Digits"))

    # create method
    @api.model
    def create(self, vals):
        print("values before create_______________", vals)
        seq = self.env['ir.sequence'].next_by_code('travel.sequence')
        print("seq_______________", seq)
        result = super(Travel, self).create(vals)
        result.travel_seq_id = seq
        print("result_______", result)
        return result
    
    # write mthod
    def write(self, vals):
    # Check if 'travel_date' field is in the values being updated
        if 'travel_date' in vals:
            # If 'travel_date' is being updated, create a history record
            travel_history_obj = self.env['travel.history']
            travel_history_obj.create({
                'name': self.name,
                'history_desc': 'Travel date changed from {} to {}'.format(
                    self.travel_date, vals.get('travel_date'))
            })
        # Call super() to perform the actual write operation
        result = super(Travel, self).write(vals)
        return result
    

    # default get method
    @api.model
    def default_get(self, fields):
        result = super(Travel, self).default_get(fields)
        # seq = self.env['ir.sequence'].next_by_code('travel.sequence')
        result.update({'ticket': 50})
        # result.update({'ticket': 50, 'travel_seq_id': seq})
        return result

    # name_get method
    def name_get(self):
        result = []
        for trav in self:
            name = ""
            name = trav.name
            if trav.travel_seq_id:
                name += trav.travel_seq_id
            if trav.name:
                name += ' ' + trav.name
            result.append((trav.id, name))
        return result
    
    # search button practise in terminal output
    def search_data(self):
        # search_var = self.env['travelling.data'].search([])
        search_var = self.env['travelling.data'].search([('ticket','<',200.00)])
        # search_var = self.env['travelling.data'].search([('ticket','<',200.00),('good_place','=','type1')])
        # search_var = self.env['travelling.data'].browse([('good_place','=','type1')])
        print("Search var______________", search_var)
        # for rec in search_var:
        #     print("name_______________", rec.name)
        #     print("mobile_______________", rec.mobile)
        #     print("travel_distance_______________", rec.travel_distance)
        #     print("ticket_______________", rec.ticket)


    # history button count
    @api.depends('travel_date')
    def get_history_count(self):
        for rec in self:
            history_count = self.env['travel.history'].search_count([('name', '=', rec.name)])
            rec.history_count = history_count  


    # history button count action
    def action_view_history(self):
        history_rec = self.env['travel.history'].search([('name','=',self.name)])
        return{
            'type':"ir.actions.act_window",
            'view_mode':'tree',
            'res_model':'travel.history',
            'target':'current',
            'domain':[('id','in',history_rec.ids)]
        } 
    

    def make_good_place(self):
        for record in self:
            if record.good_place == 'type2':
                record.write({'good_place': 'type1'})


class TravelHistory(models.Model):
    _name = "travel.history"
    _description="Travel History"

    name = fields.Char()
    history_desc = fields.Char()