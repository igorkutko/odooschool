from odoo import api, fields, models


class DiseaseReport(models.TransientModel):
    _name = 'hr_hospital.disease_report'
    _description = 'Disease report'
    _rec_name = 'diagnosis_date'

    period_year = fields.Integer()
    period_month = fields.Integer()
    diagnosis_date = fields.Date()
    disease_id = fields.Many2one(comodel_name='hr_hospital.disease')
    diagnosis_id = fields.Many2one(comodel_name='hr_hospital.diagnosis')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient')
    disease_count = fields.Integer()

    @property
    def _table_query(self):
        query = f'{self._select()} {self._from()}'
        return query

    @api.model
    def _select(self):
        select_clause = """
            SELECT
                diagnosis.id AS id,
                diagnosis.id AS diagnosis_id,
                diagnosis.diagnosis_date AS diagnosis_date,
                EXTRACT(year from diagnosis.diagnosis_date) AS period_year,
                EXTRACT(month from diagnosis.diagnosis_date) AS period_month,
                diagnosis.disease_id AS disease_id,
                diagnosis.doctor_id AS doctor_id,
                diagnosis.patient_id AS patient_id,
                1 AS disease_count
        """
        return select_clause

    @api.model
    def _from(self):
        from_clause = """
            FROM
                hr_hospital_diagnosis AS diagnosis
        """
        return from_clause

    def _where(self):
        self.ensure_one()
        where_clause = """
            WHERE
                TRUE
        """
        return where_clause
