from mongoengine import DictField, Document, IntField, ListField, StringField


class ProductMetadataModel(Document):
    meta = {
        "collection": "product_metadata",
        "indexes": ["product_id"],
        "ordering": ["-product_id"],
        "strict": False,
    }

    product_id = IntField(required=True, unique=True)
    name = StringField(required=True, max_length=150)
    tags = ListField(StringField(max_length=50), default=list)
    specifications = DictField(default=dict)
    care_instructions = StringField()
    seo_title = StringField(max_length=150)
    seo_description = StringField(max_length=300)
    vendor_notes = StringField()
