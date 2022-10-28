from odoo import fields, models


class PatientCard(models.Model):
    _name = 'hr_hospital.patient_card'
    _description = 'Patient card'

    name = fields.Char()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
