from odoo import http
from odoo.http import request

class OpenAcademy(http.Controller):

    @http.route('/hello', auth="public")
    def hello(self, **kw):
        return "Hello World"

    @http.route('/hello_user', auth="user")
    def hello_user(self, **kw):
        return "Hello %s" %(request.env.user.name)

    @http.route('/hello_template')
    def hello_template(self, **kw):
        return request.render('estate.hello_world')

    @http.route('/hello_template_user')
    def hello_template_user(self, **kw):
        properties = request.env['estate.property'].search([('state', '=', 'new')])
        print ("properties ::: ", properties)
        return request.render('estate.hello_user', { 'user': request.env.user, 'properties': properties })   

    # @http.route('/property', auth="public", website=True)
    # def property(self, **kw):
    #     return request.render('estate.properties_static',{

    #         'properties': request.env['estate.property'].sudo().search([], limit=8)

    #     }) 

    @http.route('/property',website=True,auth='public')
    def estate_porperty_show(self,**kw):
        # return "property page"

        properties = request.env['estate.property'].search([])
        return request.render("estate.properties_static",{

                'properties':properties,


        })
