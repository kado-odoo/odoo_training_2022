from odoo import fields, models


class EstateWizard(models.TransientModel):
    _name = 'estate.wizard'
    _description = 'Estate Wizard'

    partner_id = fields.Many2one('res.partner')
    price = fields.Float()
    #property_type_id = fields.Many2one('estate.property.type')


    def action_make_offer(self):
        # self.ensure_one()
        # offer = self.env['estate.property.offer']
        activeIds = self.env.context.get('active_ids')
        for i in activeIds:
            self.env['estate.property.offer'].create({'price':self.price , 'partner_id':self.partner_id.id})
        return True
        # data = {
        #     'partner_id' : self.partner_id,
        #     'price' : self.price,
        #     'property_type_id' : self.property_type_id
        # }
        # for property in self.env['estate.property'].browse(activeIds):
        #     data['property_id']=property.id
        #     offer.create(data)