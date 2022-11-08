from odoo import fields, models


class SampleType(models.Model):
    _name = 'hr_hospital.sample_type'
    _description = 'Sample type'

    name = fields.Char()
