"""
Regression tests for set_vanilla_runesanity_rules in Rules.py. These use add_rule to
AND extra rune requirements onto the existing vanilla level-progression entrance rules.
Only a representative sample is covered here (not every one of the ~19 entrances this
function touches), since they all follow the same has_required_runes(...) pattern.
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions, RuneSanityToggle


class VanillaRunesanityTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.VANILLA,
        "runesanity": RuneSanityToggle.option_true,
    }

    def test_the_graveyard_requires_dans_crypt_star_rune(self) -> None:
        # Runesanity puts a rune block on "Cleared: Dan's Crypt", which every vanilla
        # "Map -> X" chain starts from.
        self.assertFalse(self.can_reach_entrance("Map -> The Graveyard"))
        self.collect_by_name("Star Rune: Dan's Crypt")
        self.assertTrue(self.can_reach_entrance("Map -> The Graveyard"))

    def test_cemetery_hill_requires_the_graveyards_two_runes(self) -> None:
        # Cleared: The Graveyard is blocked behind Chaos Rune: The Graveyard, which is itself
        # blocked behind Earth Rune: The Graveyard.
        self.collect_by_name("Star Rune: Dan's Crypt")
        self.assertFalse(self.can_reach_entrance("Map -> Cemetery Hill"))
        self.collect_by_name("Earth Rune: The Graveyard")
        self.assertFalse(self.can_reach_entrance("Map -> Cemetery Hill"))
        self.collect_by_name("Chaos Rune: The Graveyard")
        self.assertTrue(self.can_reach_entrance("Map -> Cemetery Hill"))

    def test_return_to_the_graveyard_stacks_runes_on_top_of_the_weapon_requirements(self) -> None:
        # Cleared: The Hilltop Mausoleum needs a club/hammer, a ranged weapon AND both the
        # Earth and Chaos runes from the Hilltop Mausoleum.
        self.collect_by_name(["Star Rune: Dan's Crypt", "Earth Rune: The Graveyard", "Chaos Rune: The Graveyard"])
        self.collect_by_name(["Equipment: Club", "Equipment: Daggers"])
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name(["Moon Rune: The Hilltop Mausoleum", "Earth Rune: The Hilltop Mausoleum"])
        self.assertFalse(self.can_reach_entrance("Map -> Return to the Graveyard"))
        self.collect_by_name("Chaos Rune: The Hilltop Mausoleum")
        self.assertTrue(self.can_reach_entrance("Map -> Return to the Graveyard"))
