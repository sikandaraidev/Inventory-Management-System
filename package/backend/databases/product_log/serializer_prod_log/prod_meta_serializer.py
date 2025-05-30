class ProductMetadataSerializer:
    def __init__(self, data: dict):
        self.data = data

    def parse_tags(self) -> list[str]:
        tags = self.data.get("tags", "")
        if isinstance(tags, list):
            return tags
        return [tag.strip() for tag in tags.split(";") if tag.strip()]

    def parse_specifications(self) -> dict:
        spec_str = self.data.get("specifications", "")
        if isinstance(spec_str, dict):
            return spec_str
        specs = {}
        for pair in spec_str.split("|"):
            if ":" in pair:
                key, value = pair.split(":", 1)
                specs[key.strip()] = value.strip()
        return specs

    def serialize(self) -> dict:
        return {
            "product_id": self.data["product_id"],
            "name": self.data["name"],
            "tags": self.parse_tags(),
            "specifications": self.parse_specifications(),
            "care_instructions": self.data.get("care_instructions"),
            "seo_title": self.data.get("seo_title"),
            "seo_description": self.data.get("seo_description"),
            "vendor_notes": self.data.get("vendor_notes"),
        }
