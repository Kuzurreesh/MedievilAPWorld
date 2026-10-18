"""Regression tests for base-game key-item dependencies, applied in every mode."""

from . import MedievilTestBase
from ..Options import ProgressionOptions


class KeyItemDependencyTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def test_shadow_artefact_requires_safe_key_inside_sleeping_village_locked_items(self) -> None:
        """
        The location sits in The Sleeping Village Locked Items (behind the Crucifix) and
        additionally needs the Safe Key and the Landlords Bust location to be reachable.
        """
        self.assertFalse(self.can_reach_location("Key Item: Shadow Artefact - SV"))
        self.collect_by_name("Key Item: Safe Key")
        self.assertFalse(self.can_reach_location("Key Item: Shadow Artefact - SV"))
        self.collect_by_name("Key Item: Crucifix")
        self.assertTrue(self.can_reach_location("Key Item: Shadow Artefact - SV"))

    def test_crucifix_requires_landlords_bust_and_crucifix_cast(self) -> None:
        self.assertFalse(self.can_reach_location("Key Item: Crucifix - SV"))
        self.collect_by_name("Key Item: Landlords Bust")
        self.assertFalse(self.can_reach_location("Key Item: Crucifix - SV"))
        self.collect_by_name("Key Item: Crucifix Cast")
        self.assertTrue(self.can_reach_location("Key Item: Crucifix - SV"))

    def test_pools_of_the_ancient_dead_clear_requires_all_soul_helmets(self) -> None:
        self.assertFalse(self.can_reach_location("Cleared: Pools of the Ancient Dead"))
        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 8)])
        self.assertFalse(self.can_reach_location("Cleared: Pools of the Ancient Dead"))
        self.collect_by_name("Key Item: Soul Helmet 8")
        self.assertTrue(self.can_reach_location("Cleared: Pools of the Ancient Dead"))
