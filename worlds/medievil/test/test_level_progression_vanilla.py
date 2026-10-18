"""
Regression tests for the vanilla progression entrance rules (set_vanilla_level_progression
in Rules.py). Each "Map -> X" entrance only requires the previous level's "Cleared" location;
the items live on the Cleared locations (and on the "<Level> Locked Items" regions that hold
some of them), not on the Map entrances themselves.
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class VanillaLevelProgressionTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.VANILLA,
    }

    def test_full_vanilla_chain_requires_items_in_order(self) -> None:
        # Dan's Crypt, The Graveyard and Cemetery Hill clear for free, so the first four
        # entrances need no items at all.
        self.assertTrue(self.can_reach_entrance("Map -> Dan's Crypt"))
        self.assertTrue(self.can_reach_entrance("Map -> The Graveyard"))
        self.assertTrue(self.can_reach_entrance("Map -> Cemetery Hill"))
        self.assertTrue(self.can_reach_entrance("Map -> The Hilltop Mausoleum"))

        # Return to the Graveyard needs Hilltop Mausoleum cleared: a club/hammer AND a ranged weapon.
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name("Equipment: Club")
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name("Equipment: Daggers")
        self.assertTrue(self.can_reach_entrance("Map -> Return to the Graveyard"))

        # Cleared: Return to the Graveyard sits in its Locked Items region, behind the Skull Key.
        # Enchanted Earth, Scarecrow Fields, Pumpkin Gorge, Pumpkin Serpent and The Sleeping Village
        # all open from it.
        for entrance in (
            "Map -> Enchanted Earth",
            "Map -> Scarecrow Fields",
            "Map -> The Sleeping Village",
            "Map -> Pumpkin Gorge",
            "Map -> Pumpkin Serpent",
        ):
            with self.subTest(entrance=entrance, stage="before skull key"):
                self.assertFalse(self.can_reach_entrance(entrance))
        self.collect_by_name("Key Item: Skull Key")
        for entrance in (
            "Map -> Enchanted Earth",
            "Map -> Scarecrow Fields",
            "Map -> The Sleeping Village",
            "Map -> Pumpkin Gorge",
            "Map -> Pumpkin Serpent",
        ):
            with self.subTest(entrance=entrance, stage="after skull key"):
                self.assertTrue(self.can_reach_entrance(entrance))

        # Cleared: Sleeping Village sits in its Locked Items region, behind the Crucifix.
        self.assertFalse(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.assertFalse(self.can_reach_entrance("Map -> Inside the Asylum"))
        self.collect_by_name("Key Item: Crucifix")
        self.assertTrue(self.can_reach_entrance("Map -> Asylum Grounds"))
        self.assertTrue(self.can_reach_entrance("Map -> Inside the Asylum"))

        # Pools of the Ancient Dead needs Enchanted Earth cleared, which sits behind the
        # Shadow Talisman + Shadow Artefact.
        self.assertFalse(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.collect_by_name("Key Item: Shadow Talisman")
        self.assertFalse(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))
        self.collect_by_name("Key Item: Shadow Artefact")
        self.assertTrue(self.can_reach_entrance("Map -> Pools of the Ancient Dead"))

        # The Lake needs Pools cleared, which needs all 8 soul helmets. The Crystal Caves, The
        # Gallows Gauntlet and The Haunted Ruins then open as a chain; the Haunted Ruins entrance
        # itself needs Dragon Armour in vanilla non-runesanity.
        self.assertFalse(self.can_reach_entrance("Map -> The Lake"))
        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 9)])
        self.assertTrue(self.can_reach_entrance("Map -> The Lake"))
        self.assertTrue(self.can_reach_entrance("Map -> The Crystal Caves"))
        self.assertTrue(self.can_reach_entrance("Map -> The Gallows Gauntlet"))
        self.assertFalse(self.can_reach_entrance("Map -> The Haunted Ruins"))
        self.collect_by_name("Equipment: Dragon Armour")
        self.assertTrue(self.can_reach_entrance("Map -> The Haunted Ruins"))

        # Cleared: The Haunted Ruins needs the crown; everything after it only needs the
        # previous level cleared (Ghost Ship also needs a club, already held).
        self.assertFalse(self.can_reach_entrance("Map -> The Ghost Ship"))
        self.collect_by_name("Key Item: King Peregrine's Crown")
        self.assertTrue(self.can_reach_entrance("Map -> The Ghost Ship"))
        self.assertTrue(self.can_reach_entrance("Map -> The Entrance Hall"))
        self.assertTrue(self.can_reach_entrance("Map -> The Time Device"))
        self.assertTrue(self.can_reach_entrance("Map -> Zaroks Lair"))

    def test_return_to_the_graveyard_accepts_hammer_as_alternative_to_club(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name(["Equipment: Hammer", "Equipment: Daggers"])
        self.assertTrue(self.can_reach_entrance("Map -> Return to the Graveyard"))
