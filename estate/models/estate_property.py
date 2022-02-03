from bdb import set_trace
from operator import truediv
from time import clock_settime
from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

#estate Prooerty Type Class

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [('postive_price', 'check(expected_price >0)', 'Enter positive value')]


    name = fields.Char(string="Property Type", default="Unknown", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

#estate Property Tag Class

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    name = fields.Char(string="Property Tag", default="Unknown", required=True)

#estate Property Offer Class

class EstatePropertyOffer(models.Model):
    _name ='estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refuse', 'Refused')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    my_property_ids =  fields.Many2one('estate.myproperty')

    #Button Method Call in Offer Table
    def action_accepted(self):
        for record in self:
            record.status = 'accepted'


    def action_refused(self):
        for record in self:
            record.status = 'refuse'

# Res Partner Class and inherit res.partener
class ResPartner(models.Model):
    _inherit = 'res.partner'

    buyer_property_id = fields.One2many('estate.property', 'buyer_id')
    is_buyer = fields.Boolean()

    offer_ids = fields.One2many('estate.property.offer', 'partner_id')

# Estate My property Class
class MyProperty(models.Model):
    _name = "estate.myproperty"    

    name = fields.Char()

    property_offer_ids = fields.One2many('estate.property.offer' , 'my_property_ids')
    partner_id = fields.Many2one('res.partner')


# Estate Property Class
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'real estate module'

    #Curent User Show in Description
    def _get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name + "'s Property"      


    name = fields.Char(string="Name", default="Unknown", required=True)
    description = fields.Text(default=_get_description)
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Datetime.now(), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')        
        ])
    #active = fields.Boolean(default=True)
    image = fields.Image()  

    #relestional fields
    #   
    property_type_id = fields.Many2one('estate.property.type',string="Property Type")
    property_tag_ids = fields.Many2many('estate.property.tag',string="Property Tag")
    #property_type_ids = fields.One2many('estate.property.type', 'property_id', string="property Type")
    state = fields.Selection([('new', 'New'), ('sold', 'Sold'), ('cancel', 'Cancelled')], default='new')
    total_area = fields.Float(compute='_compute_area',inverse='_inverse_area')
    best_price = fields.Float(compute="_compute_best_price", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id')
    salesman_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner')

    #accsept Offer method call in button
    def open_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "views": [[view_id, 'tree']],
            # "res_id": 2,
            "target": "new",
            "domain": [('property_id', '=', self.id)]
        }
    def confirm_offers(self):
        view_id = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "views": [[view_id, 'tree']],
            "target": "new",
            "domain": [('status', '=', 'accepted')]
        }

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:

            record.date_deadline = fields.Date.add(record.date_availability, days=record.validity)
            #date_availability

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):  # Recordset [ Collection  of records]
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price

    def action_sold(self):
        # print("\n\n In action sold")
        for record in self:
            if record.state == 'cancel':
                raise UserError("Cancel Property cannot be sold")
            record.state = 'sold'
            # return some action

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold Property cannot be canceled")
            record.state = 'cancel'

    @api.depends('living_area','garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area=record.living_area + record.garden_area


    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2



    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")


    @api.onchange("garden")
    def _onchange_partner_id(self):
        for record in self:
            if record.garden:
                record.garden_area=10
                record.garden_orientation='north'
            else:
                record.garden_area=None
                record.garden_orientation=None

    # @api.model
    # def create(self,vals):
    #     print("\n\nHello kamla",vals)

    # Overriding methods
    # @api.model
    # def create(self, vals):
    #     # vals is a dict of all fields with values or default values  -> insert
    #     # vals['name'] = uppercase
    #     print("\n Create method is called ", vals)
    #     # vals['ref_seq'] = "Prop/123"
    #     if vals.get('ref_seq', 'New') == 'New':
    #         vals['ref_seq'] = self.env['ir.sequence'].next_by_code('property.seq')

    #     t = super(EstateProperty, self).create(vals)
    #     return t

       

    # @api.model
    # def create(self,vals):
    #     vals = {'name': 'XYZ', 'expected_price':'30'}
    #     res = super(EstateProperty, self).create(vals)
    #     return res

    # def write(self, vals):
    #     # dict of changed field -> update
    #     print("\n Write method is called ", vals)
    #     return super(EstateProperty, self).write(vals)
       




