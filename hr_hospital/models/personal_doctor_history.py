from odoo import api, fields, models


class PersonalDoctorHistory(models.Model):
    _name = 'hr_hospital.personal_doctor_history'
    _description = 'History of personal doctor'

    name = fields.Char()
    appointment_date = fields.Date()
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
