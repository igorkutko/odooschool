from datetime import datetime, timedelta
from odoo.exceptions import AccessError
from odoo.tests import tagged
from odoo.tests.common import new_test_user, TransactionCase


@tagged('post_install', '-at_install', 'visit', 'access_right')
class TestAccessRightVisit(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_admin = cls.env.ref('base.user_admin')
        cls.test_user = new_test_user(cls.env, login='test_user', groups='base.group_user')
        cls.test_trainee = new_test_user(
            cls.env,
            login='test_trainee',
            groups='hr_hospital.hr_hospital_group_trainee'
        )

    def create_patient(self, user, **values):
        return self.env['hr_hospital.patient'].with_user(user).create({
            'name': 'test_patient',
            **values
        })

    def create_doctor(self, user, **values):
        return self.env['hr_hospital.doctor'].with_user(user).create({
            'name': 'test_doctor',
            **values
        })

    def create_visit(self, user, **values):
        one_hour = timedelta(hours=1)
        return self.env['hr_hospital.visit'].with_user(user).create({
            'name': 'test_visit',
            'visit_date': datetime.now(),
            'visit_stop_date': datetime.now() + one_hour,
            **values

        })

    def test_check_access_user(self):
        test_patient1 = self.create_patient(self.test_admin)
        test_doctor1 = self.create_doctor(self.test_admin)
        with self.assertRaises(AccessError, msg='User should not able to create a visit!'):
            self.create_visit(
                self.test_user,
                patient_id=test_patient1.id,
                doctor_id=test_doctor1.id
            )

    def test_check_access_trainee(self):
        test_patient1 = self.create_patient(self.test_admin)
        test_doctor1 = self.create_doctor(self.test_admin)
        one_hour = timedelta(hours=1)
        one_day = timedelta(days=1)
        visit_date = datetime.now() - one_day * 40
        visit_stop_date = visit_date + one_hour
        test_visit1 = self.create_visit(
            self.test_admin,
            visit_date=visit_date,
            visit_stop_date=visit_stop_date,
            patient_id=test_patient1.id,
            doctor_id=test_doctor1.id
        )
        with self.assertRaises(AccessError, msg='Trainee should not able to change a visit older than 30 days!'):
            test_visit1.with_user(self.test_trainee).write({'name': 'changed by trainee'})
