# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class order(models.Model):
    _name = 'coffee.order'
    _description = 'coffee_order'

    customer = fields.Many2one("res.partner", ondelet="set null", string="customer name",
                               required=True)
    date = fields.Date(string="date", default=datetime.today())
    number = fields.Char(string="Task No", readonly=True, copy=False, default='New')
    description = fields.Text(string="description")
    line_ids = fields.One2many("order.line", "order_id", string="line_id")

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('coffe.order')
        result = super(order, self).create(vals)
        return result


class product(models.Model):
    _name = 'order.line'
    _description = 'order_line'

    product_id = fields.Many2one("product.product", string="name of product",
                                 ondelete='set null')

    quantity = fields.Float(string="quantity", default=1.00)
    price = fields.Float(string="price")
    discount = fields.Float(string="discount", readonly=True, store=True)
    total = fields.Float(string="total", compute="_total_price")
    order_id = fields.Many2one("coffee.order", string="order_id")

    @api.depends('price', 'quantity')
    def _total_price(self):
        for r in self:
            if r.quantity > 2:
                r.total = r.price * r.quantity - r.price * .1
                r.discount = r.price * .1
            else:
                r.total = r.price * r.quantity
                r.discount = 0.00

    @api.onchange('product_id')
    def _price_change(self):
        self.price = self.product_id.list_price

    # @api.onchange('amount')
    # def _discount_change(self):
    #

# class promotion(models.Model):
#     _name = 'sale.promotion'
#     _description = 'sale_promotion'
#
#     product = fields.Many2one("product.product", string="name of product",
#                               ondelete='set null')
#
#     quantity = fields.Float(string="quantity", default=1.00)
#     price = fields.Float(string="price")
#     total = fields.Float(string="total", compute="_total_price")
#     discount = fields.Float(string="discount", compute="_disc_", store=True)
#     order_id = fields.Many2one("coffee.order", string="order_id")
