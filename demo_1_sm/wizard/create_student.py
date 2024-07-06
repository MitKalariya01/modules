
from datetime import date

from odoo import models, fields, api


class create_student_wizard(models.Model):
    _name = 'create.student.wizard'
    _description = 'Create Student Wizard'
    _rec_name = 'name'

    name = fields.Char(string='Name', required="1")
    mobile = fields.Char(string='Mobile', required="1")
    email = fields.Char(string='Email', required="1")
    date_of_birth = fields.Date(string='Date of Birth', required="1")
    age = fields.Integer(string="Age")
    image = fields.Image(string="Student Image")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender",
                              default='male', required="1")

    class_id = fields.Many2one('leap.class.class', string="Class", required="1")

    @api.onchange('date_of_birth')
    def calculate_age(self):
        if self.date_of_birth:
            self.age = date.today().year - self.date_of_birth.year

    def button_action_create_student(self):
        vals = {
            'student_name': self.name,
            'student_mobile': self.mobile,
            'student_email': self.email,
            'date_of_birth': self.date_of_birth,
            'age': self.age,
            'student_image': self.image,
            'gender': self.gender,
            'class_id': self.class_id.id,
        }
        student_id = self.env['leap.student.student'].create(vals)

        action = self.env['ir.actions.actions']._for_xml_id('l4l_school_management_demo.action_leap_all_student')

        if len(student_id) > 1:
            action['domain'] = [('id', 'in', student_id.ids)]
        elif len(student_id) == 1:
            form_view = [(self.env.ref('l4l_school_management_demo.view_leap_student_student_form').id, 'form')]

            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view

            action['res_id'] = student_id.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
            return action

        # context = {
        #     'default_student_id': self.id,
        # }
        # action['context'] = context
        return action

