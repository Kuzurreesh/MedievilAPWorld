"""
Regression tests for the open progression entrance rules (set_open_level_progression in
Rules.py). Every "Map -> X" entrance only requires Dan's Crypt to be cleared, which needs
no items. The one exception is Inside the Asylum, which also needs any weapon. Item
requirements live on the Cleared locations and Locked Items regions instead.
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class OpenLevelProgressionTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_entrances_other_than_inside_the_asylum_are_open_from_the_start(self) -> None:
        for entrance in (
            "Map -> Dan's Crypt",
            "Map -> The Graveyard",
            "Map -> Return to the Graveyard",
            "Map -> Cemetery Hill",
            "Map -> The Hilltop Mausoleum",
            "Map -> Scarecrow Fields",
            "Map -> The Crystal Caves",
            "Map -> The Lake",
            "Map -> Pumpkin Gorge",
            "Map -> Pumpkin Serpent",
            "Map -> The Sleeping Village",
            "Map -> Pools of the Ancient Dead",
            "Map -> Asylum Grounds",
            "Map -> Enchanted Earth",
            "Map -> The Gallows Gauntlet",
            "Map -> The Haunted Ruins",
            "Map -> The Ghost Ship",
            "Map -> The Entrance Hall",
            "Map -> The Time Device",
            "Map -> Zaroks Lair",
        ):
            with self.subTest(entrance=entrance):
                self.assertTrue(self.can_reach_entrance(entrance))

    def test_inside_the_asylum_requires_any_weapon(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Inside the Asylum"))
        self.collect_by_name("Equipment: Club")
        self.assertTrue(self.can_reach_entrance("Map -> Inside the Asylum"))

    def test_item_requirements_sit_on_cleared_locations_not_entrances(self) -> None:
        self.assertFalse(self.can_reach_location("Cleared: Pools of the Ancient Dead"))
        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 9)])
        self.assertTrue(self.can_reach_location("Cleared: Pools of the Ancient Dead"))

        self.assertFalse(self.can_reach_location("Cleared: The Haunted Ruins"))
        self.collect_by_name("Key Item: King Peregrine's Crown")
        self.assertFalse(self.can_reach_location("Cleared: The Haunted Ruins"))
        self.collect_by_name("Skill: Daring Dash")
        self.assertTrue(self.can_reach_location("Cleared: The Haunted Ruins"))

        self.assertFalse(self.can_reach_location("Cleared: Ghost Ship"))
        self.collect_by_name("Equipment: Club")
        self.assertTrue(self.can_reach_location("Cleared: Ghost Ship"))
