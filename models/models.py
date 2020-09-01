# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class order(models.Model):
    _name = 'coffee.order'
    _description = 'coffee_order'

    customer = fields.Many2one("res.partner", ondelet="set null", string="customer name",
                               required=True)
    date = fields.Date(string="date", default=datetime.today())
    number = fields.Char(string="number")
    description = fields.Text()
    line_ids = fields.One2many("order.line", "order_id", string="line_id")


class product(models.Model):
    _name = 'order.line'
    _description = 'order_line'

    product_id = fields.Many2one("product.product", string="name of product", change_default=True,
                                 ondelete='restrict')

    quantity = fields.Float(string="quantity", default=1.00)
    price = fields.Float(string="price", related="product_id.list_price")
    Total = fields.Float(string="total", compute="_total_price")
    order_id = fields.Many2one("coffee.order", string="order_id")

    @api.depends('price', 'quantity')
    def _total_price(self):
        for r in self:
            r.Total = r.price * r.quantity
