from odoo import models, fields


class leap_class_class(models.Model):
    _name = 'leap.class.class'
    _description = 'Leap Class'
    _rec_name = 'class_name'

    class_name = fields.Char(string='Name', required="1")
    class_student = fields.One2many('leap.student.student', 'class_id', string='Students')

    student_count = fields.Integer(string="Total Students", compute="count_student")

    def count_student(self):
        for record in self:
            record.student_count = self.env['leap.student.student'].search_count([('class_id', '=', record.id)])

    # CODE OF SMART BUTTON

    """def action_view_student_detail(self):
        student_ids = self.env['leap.student.student'].search([('class_id', '=', self.id)])
        action = self.env['ir.actions.actions']._for_xml_id('l4l_school_management_demo.action_leap_all_student')

        if len(student_ids) > 1:
            action['domain'] = [('id', 'in', student_ids.ids)]
        elif len(student_ids) == 1:
            form_view = [(self.env.ref('l4l_school_management_demo.view_leap_student_student_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = student_ids.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
            return action

        context = {'default_class_id': self.id}
        action['context'] = context
        return action"""

