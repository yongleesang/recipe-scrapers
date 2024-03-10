# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._grouping_utils import group_ingredients
from ._utils import get_equipment
from ._utils import get_minutes, get_yields, normalize_string

class BudgetBytes(AbstractScraper):
    @classmethod
    def host(cls):
        return "budgetbytes.com"

    def title(self):
        return self.schema.title()

    def author(self):
        return self.schema.author()

    def total_time(self):
        return self.schema.total_time()

    def yields(self):
        return self.schema.yields()

    def ingredients(self):
        # return self.schema.ingredients()
        def get_ingredient_text(item, key):
            span = item.find("span", "wprm-recipe-ingredient-" + key)
            return normalize_string(span.text) if span else ""

        ingredients_list = []
        keys = ["amount", "unit", "name"]
        for item in self.soup.select("li.wprm-recipe-ingredient"):
            ingredient_parts = [get_ingredient_text(item, key) for key in keys]
            print(ingredient_parts)
            #ingredients_list.append(" ".join(filter(None, ingredient_parts)))
            ingredients_list.append(ingredient_parts)
            
        return ingredients_list
    
    def ingredient_groups(self):
        return group_ingredients(
            self.ingredients(),
            self.soup,
            ".wprm-recipe-ingredient-group h4",
            ".wprm-recipe-ingredient",
        )

    def instructions(self):
        return self.schema.instructions()

    def ratings(self):
        return self.schema.ratings()

    def equipment(self):
        equipment_items = [
            link.get_text()
            for link in self.soup.select(
                "div.wprm-recipe-equipment-name a.wprm-recipe-equipment-link"
            )
        ]
        return get_equipment(equipment_items)
