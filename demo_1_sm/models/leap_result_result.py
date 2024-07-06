
from odoo import models, fields, api, _


class leap_result_result(models.Model):
    _name = 'leap.result.result'
    _description = 'Leap Result'
    _rec_name = 'student_id'

    number = fields.Char('Sequence', copy=False, default='New')
    student_id = fields.Many2one('leap.student.student', string='Student', required="1", ondelete='restrict')
    image = fields.Image(string="Student Image")
    student_class_name = fields.Many2one('leap.class.class', string='Class')
    result_student_mobile = fields.Char(string='Mobile')
    result_student_email = fields.Char(string='Email')
    result_student_date_of_birth = fields.Char(string='Date of Birth')
    result_list = fields.One2many('leap.result.lines', 'result_id', string='Result')
    total = fields.Float(string="Total", compute="count_total", store=True)
    percentage = fields.Float(string="Percentage", readonly="1")
    age = fields.Integer(related='student_id.age', readonly=False, store=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], string="State",
                             default="draft")

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('number', _("New")) == _("New"):
                val['number'] = self.env['ir.sequence'].next_by_code('leap.result.result') or _("New")

        return super().create(vals_list)

    @api.depends('result_list', 'result_list.subject_marks')
    def count_total(self):
        for record in self:
            if record.result_list:
                tot = 0
                for marks in record.result_list:
                    tot += marks.subject_marks if marks.subject_marks else 0

                record.total = tot
                record.percentage = record.total / len(record.result_list)
            else:
                record.total = record.percentage = 0

    @api.onchange('student_id')
    def on_change_student_id(self):
        if self.student_id:
            self.student_class_name = self.student_id.class_id.id
            self.result_student_mobile = self.student_id.student_mobile
            self.result_student_email = self.student_id.student_email
            self.result_student_date_of_birth = self.student_id.date_of_birth
            self.image = self.student_id.student_image

    def test_button(self):
        if self.number == 'New':
            self.number = self.env['ir.sequence'].next_by_code('leap.result.result') or _("New")
        nm = self.student_id.test_student()
        nm2 = self.env['leap.student.student'].test_student()
        print(f"\n\nnm=============={nm}\nnm2=================={nm2}\n\n")

        for record in self:
            if record.result_list:
                for rec in record.result_list:
                    print(f"{rec.subject_id.subject_name}\t==>\t{rec.subject_marks}")
        print()
        print()

    def action_confirm(self):
        self.state = 'confirm'

        if self.state == 'confirm':
            if self.number == 'New':
                self.number = self.env['ir.sequence'].next_by_code('leap.result.result') or _("New")

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def default_get(self, fields):
        result = super(leap_result_result, self).default_get(fields)

        vals = [(0, 0, {'subject_id': 1, 'subject_marks': 55}),
                (0, 0, {'subject_id': 2, 'subject_marks': 75}),
                (0, 0, {'subject_id': 3, 'subject_marks': 64}),
                (0, 0, {'subject_id': 4, 'subject_marks': 81})]
        result.update({'result_list': vals})
        return result


