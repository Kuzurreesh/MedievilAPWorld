"""
Regression tests for the add_item_rule exclusions set up in MedievilWorld.set_rules()
(worlds/medievil/__init__.py). These control which items the fill algorithm is allowed
to place at a location, independent of access rules.
"""

from . import MedievilTestBase


class ItemPlacementRulesTest(MedievilTestBase):
    def _item_allowed(self, location_name: str, item_name: str) -> bool:
        location = self.multiworld.get_location(location_name, self.player)
        item = self.world.create_item(item_name)
        return location.item_rule(item)

    def test_dans_crypt_excludes_hammer_club_and_daring_dash(self) -> None:
        location_name = "Life Bottle: Dan's Crypt"
        for excluded in ("Equipment: Hammer", "Equipment: Club", "Skill: Daring Dash"):
            with self.subTest(item=excluded):
                self.assertFalse(self._item_allowed(location_name, excluded))
        self.assertTrue(self._item_allowed(location_name, "Gold Coins (50)"))

    def test_locked_items_dc_excludes_hammer_club_and_daring_dash(self) -> None:
        location_name = "Life Bottle: Dan's Crypt - Behind Wall"
        for excluded in ("Equipment: Hammer", "Equipment: Club", "Skill: Daring Dash"):
            with self.subTest(item=excluded):
                self.assertFalse(self._item_allowed(location_name, excluded))
        self.assertTrue(self._item_allowed(location_name, "Gold Coins (50)"))

    def test_skull_key_is_no_longer_excluded_from_locked_items_locations(self) -> None:
        """
        The skull-key exclusion for the Locked Items regions is commented out in __init__.py,
        since the logic now handles it, so the skull key can be placed in all of them.
        """
        for location_name in (
            "Life Bottle: Dan's Crypt - Behind Wall",
            "Equipment: Copper Shield in Arena - CH",
            "Gold Coins: Gold Chest at Phantom of the Opera 1 - HM",
            "Gold Coins: Chest Next to Chalice - SF",
            "Energy Vial: Near Chalice - SV",
        ):
            with self.subTest(location=location_name):
                self.assertTrue(self._item_allowed(location_name, "Key Item: Skull Key"))

    def test_weapon_and_dash_exclusions_do_not_apply_outside_dans_crypt(self) -> None:
        location_name = "Equipment: Copper Shield in Arena - CH"
        self.assertTrue(self._item_allowed(location_name, "Equipment: Club"))
        self.assertTrue(self._item_allowed(location_name, "Skill: Daring Dash"))

    def test_chalice_reward_excludes_all_key_items(self) -> None:
        location_name = "Chalice Reward 1"
        self.assertFalse(self._item_allowed(location_name, "Key Item: Skull Key"))
        self.assertFalse(self._item_allowed(location_name, "Key Item: Witches Talisman"))
        self.assertTrue(self._item_allowed(location_name, "Gold Coins (50)"))
        self.assertTrue(self._item_allowed(location_name, "Equipment: Club"))
