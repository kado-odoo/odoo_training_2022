from odoo import models,fields,api

# class EstatePropertyExtend(models.Model):
# _inherit = 'estate.property'

# expected_price = fields.Float(required=True)

class EstatePropertyExtend(models.Model):
    _inherit = 'estate.property'
    
    additional_details = fields.Text()

class LeaseProperty(models.Model):
    _name = 'lease.property'
    _inherits = {'estate.property':'property_id'}

    property_id = fields.Many2one('estate.property')
    lease_duration = fields.Date()
    lease_rent_monthly = fields.Float()