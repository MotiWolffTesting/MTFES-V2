from pathlib import Path


class WeaponsExtractor:
    def __init__(self):
        current_dir = Path(__file__).parent
        weapon_file = current_dir.parent / "weapon_list.txt"

        with open(weapon_file, "r", encoding="utf-8") as f:
            self._weapon_list = f.read().splitlines()

    def extract_weapons(self, text: str) -> list[str]:
        return [weapon for weapon in self._weapon_list if weapon in text.lower()]