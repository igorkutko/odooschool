from odoo import api, fields, models


class BulkPersonalDoctor(models.TransientModel):
    _name = 'hr_hospital.bulk_personal_doctor'
    _description = 'Bulk personal doctor'

    def _default_patient_ids(self):
        patient_manager = self.env['hr_hospital.patient']
        active_ids = self._context.get('active_ids')
        default_patient_ids = patient_manager.browse(active_ids)
        return default_patient_ids

    personal_doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    patient_ids = fields.Many2many(
        comodel_name='hr_hospital.patient',
        default=_default_patient_ids
    )

    def bulk_personal_doctor(self):
        self.ensure_one()
        patient_vals = {
            'personal_doctor_id': self.personal_doctor_id.id,
        }
        if self.patient_ids:
            patient_recs = self.patient_ids
        else:
            patient_recs = self.env['hr_hospital.patient'].search([])
        for rec in patient_recs:
            rec.write(patient_vals)
