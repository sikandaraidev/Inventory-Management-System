from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    DateField,
    DecimalField,
    FileField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    sku = StringField("SKU", validators=[DataRequired(), Length(max=50)])

    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    supplier_id = SelectField("Supplier", coerce=int, validators=[DataRequired()])

    cost_price = DecimalField(
        "Cost Price", validators=[DataRequired(), NumberRange(min=0)]
    )
    selling_price = DecimalField(
        "Selling Price", validators=[DataRequired(), NumberRange(min=0)]
    )
    quantity_in_stock = IntegerField(
        "Quantity in Stock", validators=[DataRequired(), NumberRange(min=0)]
    )

    expiry_date = DateField("Expiry Date", format="%Y-%m-%d", validators=[Optional()])
    description = TextAreaField("Description", validators=[Optional(), Length(max=500)])

    status = SelectField(
        "Status",
        choices=[("active", "Active"), ("inactive", "Inactive")],
        validators=[DataRequired()],
    )

    image = FileField(
        "Product Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Images only!"),
        ],
    )

    submit = SubmitField("Submit")
