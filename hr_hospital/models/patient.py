from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Patient'
    _inherit = ['hr_hospital.person']

    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')
    passport_data = fields.Char()
    contact_person_id = fields.Many2one(
        comodel_name='hr_hospital.contact_person'
    )
    personal_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor'
    )

    def write(self, vals):
        result = super(Patient, self).write(vals)

        for obj in self:
            if not vals.get('personal_doctor_id'):
                continue
            history_vals = {
                'name': obj['name'],
                'appointment_date': fields.Date.today(),
                'patient_id': obj['id'],
                'doctor_id': vals.get('personal_doctor_id'),
            }

            key_domain = [
                ('patient_id', '=', history_vals.get('patient_id')),
                ('doctor_id', '=', history_vals.get('doctor_id')),
            ]
            pd_manager = self.env['hr_hospital.personal_doctor_history']
            history_recs = pd_manager.search(key_domain)
            if history_recs:
                continue

            pd_manager.create(history_vals)

        return result

    @api.depends('birth_date')
    def _compute_age(self):
        for obj in self:
            bd = obj.birth_date
            obj.age = relativedelta(fields.Date.today(), bd).years if bd else 0
