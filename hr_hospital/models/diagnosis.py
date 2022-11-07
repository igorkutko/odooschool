from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char()
    description = fields.Char()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    patient_card_id = fields.Many2one(comodel_name='hr_hospital.patient_card')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    disease_id = fields.Many2one(comodel_name='hr_hospital.disease')
    treatment = fields.Char()
    diagnosis_date = fields.Date()
    mentor_comment = fields.Char()

    @api.constrains('doctor_id')
    def _check_mentor_comment(self):
        if self.doctor_id.is_intern and not self.mentor_comment:
            raise ValidationError(_('Mentor comment is required for intern doctor!'))
