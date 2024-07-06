

from odoo import models, fields, api, _
from datetime import date, datetime
from odoo.exceptions import ValidationError


class leap_student_student(models.Model):
    _name = 'leap.student.student'
    _description = 'Leap Student'
    _rec_name = 'student_name'

    student_id = fields.Char('Student Id', copy=False, default="New")
    student_name = fields.Char(string='Name', required="1")
    student_mobile = fields.Char(string='Mobile', required="1")
    student_email = fields.Char(string='Email', required="1")
    student_date_of_birth = fields.Date(string='Student Date of Birth')
    student_age = fields.Integer(string="Student Age")
    date_of_birth = fields.Date(string='Date of Birth', required="1")
    age = fields.Integer(string="Age")
    student_image = fields.Image(string="Student Image")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender",
                              default='male', required="1")
    class_id = fields.Many2one('leap.class.class', string="Class", required="1")
    result_line = fields.One2many('leap.result.result', 'student_id', string="Results")
    result_count = fields.Integer(string="Total Result", compute="count_result")
    subject_ids = fields.Many2many('leap.subject.subject', string="Subject", widget="many2many_tags")


    # create function to calculate age
    def calculate_age(self, birth_date):
        if type(birth_date) != date:
            birth_date = datetime.strptime(birth_date,  '%Y-%m-%d')

        return date.today().year - birth_date.year

    def test_student(self):
        return self.student_name

    def get_record_ids(self):

        # Print Student Ids in one line
        print("\n\n========================================")
        print("\tPRINT STUDENT IDS IN ONE LINE\n\n")
        if self.id == 67:
            record_id = self.env['leap.student.student'].search([('id', '=', '67')]).student_name
            print(f"Student whose id is 67:\t{record_id}")
        else:
            print("\n\n======== ID 67 IS NOT AVAILABLE ========\n\n")

        record_id = self.env['leap.student.student'].search([])
        print(f"Student ids : {record_id}")

        record_id = self.env['leap.student.student'].search([], offset=4, order="id desc")
        # record_id = self.env['leap.student.student'].search([], offset=2)
        print(f"Student ids using offset : {record_id}")

        print("\n\n================ CLOSE ================\n\n")


        # Print Result ids of current student Id
        print("\n\n========================================")
        print("\tPRINT RESULT IDS OF CURRENT STUDENT ID\n\n")

        record_id = self.env['leap.result.result'].search([], offset=1)
        print(f"Result id of {self.student_name} is using offset:\t{record_id}")

        record_id = self.env['leap.result.result'].search([('student_id', '=', self.id)])
        print(f"Result id of {self.student_name} is :\t{record_id}")

        record_id = self.env['leap.result.result'].search([('student_id', '=', self.id)], limit=1, order="id desc")
        print(f"Result id of {self.student_name} is using limit and reverse order :\t{record_id}")
        print("\n\n================ CLOSE ================\n\n")

        # Print Student Ids in one by one line
        print("\n\n========================================")
        print("\tPRINT STUDENT IDS IN ONE BY ONE LINE\n\n")
        for record in self.search([]):
            print(record)
        print("\n\n================ CLOSE ================\n\n")

        # Print Result Ids
        print("\n\n========================================")
        print("\tPRINT RESULT IDS\n\n")
        for record in self.env['leap.result.result'].search([]):
            print(record)
        print("\n\n================ CLOSE ================\n\n")

    def action_search_count(self):
        # Print Student Ids in one line
        print("\n\n========================================")
        print("\tPRINT HOW MANY RECORDS AVAILABLE OF STUDENTS\n\n")
        searches = self.env['leap.student.student'].search_count(['|', ('gender', '=', 'male'), ('gender', '=', 'female')])
        print(f"search_count :\t{searches}")
        print("\n\n================ CLOSE ================\n\n")

    def method_find_age(self):
        if self.student_date_of_birth:
            self.student_age = date.today().year - self.student_date_of_birth.year

        if self.date_of_birth:
            self.age = self.calculate_age(self.date_of_birth)  # find age through function

    # It returns record set (record id)
    @api.model_create_multi
    def create(self, vals):  # Here value represents a list of dictionary
        print(f"\nCREATE METHOD\nVALS\n================{vals}==================\n\n")

        for val in vals:  # Here value represents a dictionary
            print(f"\nCREATE METHOD\nVAL\n================{val}==================\n\n")

            # For Create Sequence Number
            if val.get('student_id', _("New")) == _("New"):
                val['student_id'] = self.env['ir.sequence'].next_by_code('leap.student.student') or _("New")

            global birth_date
            # for compute age of student at create time
            if val.get('student_date_of_birth'):
                if type(val.get('student_date_of_birth')) == str:
                    birth_date = datetime.strptime(val.get('student_date_of_birth'), '%Y-%m-%d')
                elif type(val.get('student_date_of_birth')) == date:
                    birth_date = val.get('student_date_of_birth')
                else:
                    raise ValidationError(_("Date Not Found"))

                val['student_age'] = date.today().year - birth_date.year

            if val.get('date_of_birth'):
                val['age'] = self.calculate_age(val['date_of_birth'])

        result = super(leap_student_student, self).create(vals)
        print(f"\nCREATE METHOD\nRESULT WHICH IS RETURN\n================{result}==================\n\n")
        return result

    # It returns true if changes made in values else return false
    def write(self, value):  # Here value represents an dictionary
        print(f"\nWRITE METHOD\nVALS\n================{value}================\n\n")

        result = super().write(value)

        print(f"\nWRITE METHOD\nRESULT WHICH IS RETURN\n================{result}==================\n\n")

        return result

    @api.onchange('date_of_birth')
    def check_birthdate(self):
        if self.date_of_birth == date.today():
            raise ValidationError(_("Happy birthday"))
        else:
            print("\n\n================Another Day================\n\n")

    def unlink(self):
        print(f"\nUNLINK METHOD\nSELF\n================{self}================\n\n")
        for record in self:
            if record.class_id.class_name == 'E':
                raise ValidationError(_("You can not delete"))

        result = super().unlink()

        print(f"\nUNLINK METHOD\nRESULT\n================{result}================\n\n")

        return result

    def count_result(self):
        print("\n\nCall ComputeMethod===========================")
        for record in self:
            record.result_count = self.env['leap.result.result'].search_count([('student_id', '=', record.id)])

    def action_open_result_of_student(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Results',
            'res_model': 'leap.result.result',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',  # if we can give value as 'new' then new wizard is open
        }

    @api.model
    def default_get(self, fields):
        print(f"\n\n\nFields --> {fields}")
        result = super(leap_student_student, self).default_get(fields)
        print(f"Result --> {result}\n")
        result['class_id'] = 1
        print(f"Result --> {result}\n\n\n")
        return result


