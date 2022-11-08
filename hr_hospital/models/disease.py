from odoo import fields, models


class Disease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Disease'

    name = fields.Char()
    disease_type_id = fields.Many2one(comodel_name='hr_hospital.disease_type')
