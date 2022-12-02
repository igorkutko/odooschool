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
    personal_doctor_history_ids = fields.One2many(
        comodel_name='hr_hospital.personal_doctor_history',
        inverse_name='patient_id',
        readonly=True
    )
    visit_ids = fields.One2many(
        comodel_name='hr_hospital.visit',
        inverse_name='patient_id',
        readonly=True
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hr_hospital.diagnosis',
        inverse_name='patient_id',
        readonly=True
    )
    research_ids = fields.One2many(
        comodel_name='hr_hospital.research',
        inverse_name='patient_id',
        readonly=True
    )
    visit_count = fields.Integer(compute='_compute_visit_count')
    diagnosis_count = fields.Integer(
        compute='_compute_diagnosis_count',
        store=True
    )
    research_count = fields.Integer(compute='_compute_research_count')

    def write(self, vals):
        """
        Searches and creates a record in personal doctor history
        :param vals: values od fields for creating personal doctor history
        :return result: record of personal doctor history
        """
        result = super(Patient, self).write(vals)

        for obj in self:
            if not vals.get('personal_doctor_id'):
                continue
            # values for personal doctor history
            history_vals = {
                'name': obj['name'],
                'appointment_date': fields.Date.today(),
                'patient_id': obj['id'],
                'doctor_id': vals.get('personal_doctor_id'),
            }
            # domain for searching personal doctor history
            key_domain = [
                ('patient_id', '=', history_vals.get('patient_id')),
                ('doctor_id', '=', history_vals.get('doctor_id')),
            ]
            pd_manager = self.env['hr_hospital.personal_doctor_history']

            # searching a record in personal doctor history by domain
            history_recs = pd_manager.search(key_domain)
            if history_recs:
                continue
            # creating a record in a personal doctor history
            pd_manager.create(history_vals)

        return result

    @api.depends('birth_date')
    def _compute_age(self):
        for obj in self:
            bd = obj.birth_date
            obj.age = relativedelta(fields.Date.today(), bd).years if bd else 0

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        visit_manager = self.env['hr_hospital.visit']
        for obj in self:
            domain = [('patient_id', '=', obj.id)]
            obj.visit_count = visit_manager.search_count(domain)

    @api.depends('diagnosis_ids')
    def _compute_diagnosis_count(self):
        diagnosis_manager = self.env['hr_hospital.diagnosis']
        for obj in self:
            domain = [('patient_id', '=', obj.id)]
            obj.diagnosis_count = diagnosis_manager.search_count(domain)

    @api.depends('research_ids')
    def _compute_research_count(self):
        research_manager = self.env['hr_hospital.research']
        for obj in self:
            domain = [('patient_id', '=', obj.id)]
            obj.research_count = research_manager.search_count(domain)
