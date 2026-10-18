"""
Regression tests for set_open_runesanity_rules and its helpers set_rune_blocks,
set_breakable_locations, and set_dashable_locations in Rules.py. These only touch
individual LOCATION access rules (not entrances), gating them behind rune items,
club/hammer, and/or daring dash. Only representative examples are covered here, not
every one of the hundreds of individual location assignments made by this function.
"""

from . import MedievilTestBase
from ..Options import BookSanityToggle, GargoyleSanityToggle, IncludeChalicesInChecksToggle, ProgressionOptions, RuneSanityToggle


class OpenRunesanityLocationRulesTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
        "runesanity": RuneSanityToggle.option_true,
    }

    def _unlock_map(self) -> None:
        # "Cleared: Dan's Crypt" is rune-blocked, and every open "Map -> X" entrance needs it.
        self.collect_by_name("Star Rune: Dan's Crypt")

    def test_dans_crypt_star_rune_gates_every_map_entrance(self) -> None:
        self.assertFalse(self.can_reach_entrance("Map -> The Graveyard"))
        self.collect_by_name("Star Rune: Dan's Crypt")
        self.assertTrue(self.can_reach_entrance("Map -> The Graveyard"))

    def test_rune_block_gates_a_location_behind_its_named_rune(self) -> None:
        self._unlock_map()
        # set_rune_blocks(self, ["Chaos Rune: The Graveyard", ...], "Earth Rune: The Graveyard")
        self.assertFalse(self.can_reach_location("Chaos Rune: The Graveyard"))
        self.collect_by_name("Earth Rune: The Graveyard")
        self.assertTrue(self.can_reach_location("Chaos Rune: The Graveyard"))

    def test_rune_blocks_can_chain(self) -> None:
        self._unlock_map()
        # "Cleared: The Graveyard" is gated behind "Chaos Rune: The Graveyard", which is
        # itself gated behind "Earth Rune: The Graveyard".
        self.assertFalse(self.can_reach_location("Cleared: The Graveyard"))
        self.collect_by_name("Earth Rune: The Graveyard")
        self.assertFalse(self.can_reach_location("Cleared: The Graveyard"))
        self.collect_by_name("Chaos Rune: The Graveyard")
        self.assertTrue(self.can_reach_location("Cleared: The Graveyard"))

    def test_boulder_location_requires_club_or_hammer(self) -> None:
        """
        "Earth Rune: The Hilltop Mausoleum" is in the set_boulder_locations list and is not
        itself gated by any rune block, so it needs only a club or hammer.
        """
        self._unlock_map()
        self.assertFalse(self.can_reach_location("Earth Rune: The Hilltop Mausoleum"))
        self.collect_by_name("Equipment: Hammer")
        self.assertTrue(self.can_reach_location("Earth Rune: The Hilltop Mausoleum"))

    def test_chalice_hilltop_requires_earth_and_moon_runes(self) -> None:
        self._unlock_map()
        # The chalice sits in The Hilltop Mausoleum Locked Items (Sheet Music) and is a boulder
        # location (club/hammer), on top of the Earth and Moon rune requirements.
        self.collect_by_name(["Key Item: Sheet Music", "Equipment: Club"])
        self.assertFalse(self.can_reach_location("Chalice: The Hilltop Mausoleum"))
        self.collect_by_name("Earth Rune: The Hilltop Mausoleum")
        self.assertFalse(self.can_reach_location("Chalice: The Hilltop Mausoleum"))
        self.collect_by_name("Moon Rune: The Hilltop Mausoleum")
        self.assertTrue(self.can_reach_location("Chalice: The Hilltop Mausoleum"))


class OpenRunesanityAllSanityTogglesOffSmokeTest(MedievilTestBase):
    """
    set_rune_blocks/set_breakable_locations/set_dashable_locations each guard against
    calling self.get_location(...) on locations that don't exist when booksanity,
    gargoylesanity, or chalices are turned off (those locations are skipped entirely in
    create_region). This is a smoke test that generation doesn't crash with every one of
    those toggles off at once, since it exercises every skip branch in those helpers.
    """

    options = {
        "progression_option": ProgressionOptions.OPEN,
        "runesanity": RuneSanityToggle.option_true,
        "booksanity": BookSanityToggle.option_false,
        "gargoylesanity": GargoyleSanityToggle.option_false,
        "include_chalices_in_checks": IncludeChalicesInChecksToggle.option_false,
    }

    def test_generation_does_not_crash(self) -> None:
        self.assertTrue(self.constructed)
