from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status")

    property_id = fields.Many2one(
        "real.estate.property",
        string="Property",
        required=True,
        ondelete="cascade"
    )
