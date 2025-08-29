from odoo import fields, models, api
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    status = fields.Selection([('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)

    property_id = fields.Many2one(
        "real.estate.property",
        string="Property",
        required=True,
        ondelete="cascade"
    )

    # Validity in days
    validity = fields.Integer(string="Validity (days)", default=7)

    # Computed validity date (create_date + validity)
    validity_date = fields.Date(
        string="Validity Date",
        compute="_compute_validity_date",
        inverse="_inverse_validity_date",
        store=True
    )

    @api.depends("create_date", "validity")
    def _compute_validity_date(self):
        for offer in self:
            if offer.create_date:
                offer.validity_date = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.validity_date = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_validity_date(self):
        """Allow manual update of validity_date and recompute validity days"""
        for offer in self:
            if offer.validity_date and offer.create_date:
                delta = offer.validity_date - offer.create_date.date()
                offer.validity = delta.days

    def action_accept(self):
        for offer in self:
            # Correct field name
            other_offers = offer.property_id.offers_ids - offer
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'offer_accepted'

            # Refuse all other offers
            other_offers.write({'status': 'refused'})

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The offer price must be strictly positive.")
