import json
from django.core.management.base import BaseCommand, CommandError
from foods.models import Food


class Command(BaseCommand):
    help = "Load foods from a JSON file."

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str)

    def handle(self, *args, **options):
        path = options["json_path"]
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise CommandError(f"JSON 로딩 실패: {e}")

        created, updated = 0, 0
        for row in data:
            name = row["name"].strip()
            obj, is_created = Food.objects.update_or_create(
                name=name,
                defaults={
                    "serving_g": row.get("serving_g", 100.0),
                    "kcal": row.get("kcal", 0),
                    "carb_g": row.get("carb_g", 0),
                    "protein_g": row.get("protein_g", 0),
                    "fat_g": row.get("fat_g", 0),
                    "sugar_g": row.get("sugar_g", 0),
                    "sodium_mg": row.get("sodium_mg", 0),
                },
            )
            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"완료: created={created}, updated={updated}")
        )
