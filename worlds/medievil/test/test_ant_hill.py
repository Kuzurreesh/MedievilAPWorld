"""
Regression tests for the Ant Hill entrance rules (set_ant_hill_rules_vanilla /
set_ant_hill_rules_open) in Rules.py. The "Enchanted Earth -> Ant Hill" entrance only
exists when include_ant_hill_in_checks is enabled (the default).
"""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class AntHillVanillaTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.VANILLA,
    }

    def test_requires_return_to_graveyard_cleared_and_witches_talisman(self) -> None:
        # Return to the Graveyard must be cleared: that needs a club/hammer and a ranged weapon
        # (Hilltop Mausoleum cleared) plus the skull key (Cleared: Return to the Graveyard sits
        # in its Locked Items region).
        self.assertFalse(self.can_reach_region("Ant Hill"))
        self.collect_by_name(["Equipment: Club", "Equipment: Daggers", "Key Item: Skull Key"])
        self.assertFalse(self.can_reach_region("Ant Hill"))
        self.collect_by_name("Key Item: Witches Talisman")
        self.assertTrue(self.can_reach_region("Ant Hill"))


class AntHillOpenTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_requires_only_witches_talisman(self) -> None:
        self.assertFalse(self.can_reach_region("Ant Hill"))
        self.collect_by_name("Key Item: Witches Talisman")
        self.assertTrue(self.can_reach_region("Ant Hill"))


class AntHillDisabledTest(MedievilTestBase):
    options = {
        "include_ant_hill_in_checks": 0,
    }

    def test_ant_hill_region_does_not_exist(self) -> None:
        with self.assertRaises(KeyError):
            self.world.get_region("Ant Hill")
