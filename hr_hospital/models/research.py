from odoo import api, fields, models


class Research(models.Model):
    _name = 'hr_hospital.research'
    _description = 'Research'

    name = fields.Char()
    research_type_id = fields.Many2one(comodel_name='hr_hospital.research_type')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    sample_type_id = fields.Many2one(comodel_name='hr_hospital.sample_type')
    sample = fields.Char()
    conclusion = fields.Char()
    visit_id = fields.Many2one(comodel_name='hr_hospital.visit')
    diagnosis_id = fields.Many2one(comodel_name='hr_hospital.diagnosis')
