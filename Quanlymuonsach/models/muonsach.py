# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
import datetime
from dateutil.relativedelta import relativedelta
import calendar
from odoo.exceptions import UserError, AccessError, ValidationError

class muonsach(models.Model):
    _name = 'quanlymuonsach.muonsach'

    ngaymuon = fields.Date()
    ngaytra = fields.Date()
    sv_id = fields.Many2one('quanlymuonsach.sinhvien', string='Sinh vien muon sach')
    sach_ids = fields.Many2many('quanlymuonsach.sach', string='Sach duoc muon')
    soluong  = fields.Char(compute='gioihan') # viết tên compute sai
    vipham = fields.Boolean(store=True, compute='check_vipham')
    sosachmuon = fields.Char(compute='check_muon') # viết tên compute sai
    # nên đặt tên label luôn ở trong này. không nên viết string ở xml


# ham dat tong so luong sach duoc muon
    @api.multi
    @api.depends('sach_ids')
    def gioihan(self):
        for r in self:
            if len(r.sach_ids) > 4:
                raise ValidationError(_('so luong <=4'))
            else:
                r.soluong = len(r.sach_ids)

# ham tinh ngay muon khong vuot qua 30 ngay
    @api.multi
    @api.onchange('ngaymuon')
    def layngay(self):
        for r in self:
            if r.ngaymuon:
                date_start_dt = fields.Date.from_string(r.ngaymuon)
                dt = date_start_dt + relativedelta(months=+1)
                r.ngaytra = fields.Date.to_string(dt)

# ham chek xem sach nao da duoc muon va tinh ra so sach da muon cua mot sinh vien
    @api.multi
    @api.constrains('vipham')
    def check_muon(self):
        count = 0
        for r in self:
            if r.sach_ids:
                for i in r.sach_ids:
                    if i.sate == False:
                        raise ValidationError(_('sach da duoc cho muon'))
                    if i.sate == True:
                        count = count + 1 # nên để count +=1 nhìn n chất hơn
            r.sosachmuon = count

# ham  Hiển thị danh sách những phiếu mượn đến thời gian cần thu hồi
    @api.multi
    @api.depends('sach_ids')
    def check_vipham(self):
        for r in self:
            if r.ngaytra:
                 dt = fields.Date.from_string(r.ngaytra).month - datetime.datetime.now().month
                 if dt < 0:
                     r.vipham = True
                 else:
                     r.vipham = False
                 #import datetime rồi thì để datetime.now().month




    @api.model
    def create(self, vals):
        record = super(muonsach, self).create(vals)
        # Ham tim sinh vien va dat dieu kien so sach muon cua mot ban ghi voi id sinh vien do
        sinhvien = self.search([('sv_id', '=', record.sv_id.id)])
        count = 0
        for r in sinhvien:
             dayrnet = fields.Date.from_string(r.ngaymuon)
             # d3 = fields.Date.from_string(r.ngaymuon).day
             d1 = dayrnet + relativedelta(days=+7)
             d2 = fields.Date.to_string(d1)
             dayin1week = fields.Date.from_string(d2).day
             today = datetime.datetime.now().day
             count += int(r.sosachmuon)
        if today > dayin1week:
            raise ValidationError(_('qua dieu kien ngay'))
        if count > 3 :
            raise ValidationError(_('khong duoc tao'))

        return record






