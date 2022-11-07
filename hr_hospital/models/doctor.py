from odoo import fields, models


class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'
    _inherit = ['hr_hospital.person']

    specialty = fields.Char()
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor', domain=[('is_intern', '=', False)])
