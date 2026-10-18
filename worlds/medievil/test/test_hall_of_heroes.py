from . import MedievilTestBase
from ..Options import ProgressionOptions


class HallOfHeroesOpenTest(MedievilTestBase):
    options = {
        "progression_option": ProgressionOptions.OPEN,
    }

    def _reward_reachable(self, count: int) -> bool:
        return self.can_reach_location(f"Chalice Reward {count}")

    def test_five_chalices_are_reachable_with_no_items_in_open_mode(self) -> None:
        """
        Hall of Heroes is entered through "<Level> -> Hall of Heroes" entrances, each needing
        that level cleared and its chalice reachable. With no items in open mode only Asylum
        Grounds, The Crystal Caves, The Graveyard, The Lake and The Time Device qualify.
        """
        for entrance in (
            "Asylum Grounds -> Hall of Heroes",
            "The Crystal Caves -> Hall of Heroes",
            "The Graveyard -> Hall of Heroes",
            "The Lake -> Hall of Heroes",
            "The Time Device -> Hall of Heroes",
        ):
            with self.subTest(entrance=entrance):
                self.assertTrue(self.can_reach_entrance(entrance))
        for i in range(1, 6):
            with self.subTest(reward=i):
                self.assertTrue(self._reward_reachable(i))
        self.assertFalse(self._reward_reachable(6))

    def test_reward_locations_unlock_progressively_as_chalice_count_rises(self) -> None:
        self.collect_by_name("Key Item: Witches Talisman")  # Ant Hill's chalice also needs a weapon: 5 -> 5
        self.assertTrue(self._reward_reachable(5))
        self.assertFalse(self._reward_reachable(6))

        # Club: Cemetery Hill, Inside the Asylum, Pumpkin Gorge, Pumpkin Serpent, Ghost Ship,
        # The Entrance Hall and (with the talisman) Ant Hill: 5 -> 12
        self.collect_by_name("Equipment: Club")
        self.assertTrue(self._reward_reachable(12))
        self.assertFalse(self._reward_reachable(13))

        # The Hilltop Mausoleum's clear and chalice live in its Locked Items region (Sheet Music): 12 -> 12
        self.collect_by_name("Equipment: Daggers")
        self.assertTrue(self._reward_reachable(12))
        self.assertFalse(self._reward_reachable(13))

        self.collect_by_name("Key Item: Sheet Music")  # The Hilltop Mausoleum Locked Items opens: 12 -> 13
        self.assertTrue(self._reward_reachable(13))
        self.assertFalse(self._reward_reachable(14))

        self.collect_by_name("Key Item: Skull Key")  # Return to the Graveyard Locked Items opens: 13 -> 14
        self.assertTrue(self._reward_reachable(14))
        self.assertFalse(self._reward_reachable(15))

        self.collect_by_name("Key Item: Harvester Parts")  # Scarecrow Fields: 14 -> 15
        self.assertTrue(self._reward_reachable(15))
        self.assertFalse(self._reward_reachable(16))

        self.collect_by_name("Key Item: Crucifix")  # The Sleeping Village Locked Items opens: 15 -> 16
        self.assertTrue(self._reward_reachable(16))
        self.assertFalse(self._reward_reachable(17))

        self.collect_by_name("Equipment: Dragon Armour")  # The Gallows Gauntlet: 16 -> 17
        self.assertTrue(self._reward_reachable(17))
        self.assertFalse(self._reward_reachable(18))

        self.collect_by_name(["Key Item: Crucifix Cast", "Key Item: Landlords Bust"])  # 17 -> 17
        self.assertTrue(self._reward_reachable(17))
        self.assertFalse(self._reward_reachable(18))

        self.collect_by_name(["Key Item: Shadow Talisman", "Key Item: Shadow Artefact"])  # Enchanted Earth Locked Items opens: 17 -> 18
        self.assertTrue(self._reward_reachable(18))
        self.assertFalse(self._reward_reachable(19))

        self.collect_by_name([f"Key Item: Soul Helmet {i}" for i in range(1, 9)])  # Pools of the Ancient Dead: 18 -> 19
        self.assertTrue(self._reward_reachable(19))
        self.assertFalse(self._reward_reachable(20))

        self.collect_by_name(["Key Item: King Peregrine's Crown", "Skill: Daring Dash"])  # The Haunted Ruins: 19 -> 20
        self.assertTrue(self._reward_reachable(20))


class HallOfHeroesChalicesDisabledTest(MedievilTestBase):
    options = {
        "include_chalices_in_checks": 0,
    }

    def test_hall_of_heroes_has_no_locations_and_no_entrances(self) -> None:
        region = self.world.get_region("Hall of Heroes")
        self.assertEqual(len(region.locations), 0)
        self.assertEqual(len(region.entrances), 0)
