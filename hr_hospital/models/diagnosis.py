from odoo import fields, models


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char()
    description = fields.Char()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    patient_card_id = fields.Many2one(comodel_name='hr_hospital.patient_card')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
