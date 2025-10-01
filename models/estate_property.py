from odoo import fields, models, api
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "real.estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    def _default_availability_date(self):
        return date.today() + timedelta(days=90)

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', copy=False, default=_default_availability_date)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation'
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        string='Status',
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # Buyer: use res.partner, should not be copied
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    # Salesperson: use res.users, default current user
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        default=lambda self: self.env.user,
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )

    offers_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers"
    )

    # Computed field for total area
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True
    )

    #  Computed field for best offer
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offers_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offers_ids.mapped("price"), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                # Set defaults when garden is checked
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                # Optional: clear values if unchecked
                record.garden_area = 0
                record.garden_orientation = False

    def action_cancel(self):
        """Cancel property unless already sold."""
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = "canceled"

    def action_sold(self):
        """Mark property as sold unless cancelled."""
        for record in self:
            if record.state == "canceled":
                raise UserError("A cancelled property cannot be sold.")
            record.state = "sold"

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("The expected price must be strictly positive.")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError("The selling price must be positive.")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            # Skip the check if selling price is zero (not validated yet)
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            # Selling price must be positive
            if float_compare(record.selling_price, 0.0, precision_digits=2) < 0:
                raise ValidationError("The selling price must be positive.")

            # Selling price cannot be lower than 90% of expected price
            min_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )

    def unlink(self):
        for prop in self:
            if prop.state not in ['new', 'canceled']:
                raise UserError("You can only delete properties that are New or Cancelled.")
        return super().unlink()

    def write(self, vals):
        # Prevent archiving of non-new/canceled properties
        if 'active' in vals and vals['active'] == False:
            for prop in self:
                if prop.state not in ['new', 'canceled']:
                    raise UserError("You can only archive properties that are New or Cancelled.")
        return super().write(vals)


