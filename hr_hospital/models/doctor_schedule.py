from odoo import api, fields, models
from datetime import datetime


class DoctorSchedule(models.Model):
    _name = 'hr_hospital.doctor_schedule'
    _description = 'Doctor schedule'

    name = fields.Char(compute='_compute_name', store=True)
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    reception_start_date = fields.Datetime()
    reception_end_date = fields.Datetime()

    _sql_constraints = [
        ('reception_date_uniq', 'UNIQUE(doctor_id, reception_start_date)', 'Reception start date must be unique.'),
    ]

    @api.depends('doctor_id', 'reception_start_date', 'reception_end_date')
    def _compute_name(self):
        format_str = '%d.%m.%Y %H:%M:%S'
        for obj in self:
            start_date = datetime.strftime(obj.reception_start_date, format_str) if obj.reception_start_date else ''
            end_date = datetime.strftime(obj.reception_end_date, format_str) if obj.reception_end_date else ''
            obj.name = f'{obj.doctor_id.name}: {start_date} - {end_date}'
