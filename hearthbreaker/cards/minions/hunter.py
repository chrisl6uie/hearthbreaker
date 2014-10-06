from hearthbreaker.constants import CHARACTER_CLASS, CARD_RARITY, MINION_TYPE
from hearthbreaker.effects.action import Draw, ChangeAttack, ChangeHealth, Charge
from hearthbreaker.effects.base import NewEffect, Aura
from hearthbreaker.effects.condition import MinionIsType
from hearthbreaker.effects.event import MinionPlaced, MinionDied
from hearthbreaker.effects.selector import MinionSelector
from hearthbreaker.effects.target import Owner, Self
from hearthbreaker.game_objects import MinionCard, Minion
import hearthbreaker.targeting
from hearthbreaker.cards.minions.neutral import (RiverCrocolisk, BloodfenRaptor, OasisSnapjaw, StonetuskBoar, CoreHound,
                                                 DireWolfAlpha, HauntedCreeper, IronbeakOwl, IronfurGrizzly,
                                                 JunglePanther, SilverbackPatriarch, StranglethornTiger,
                                                 YoungDragonhawk, AngryChicken, EmperorCobra, StampedingKodo,
                                                 CaptainsParrot, HungryCrab, KingMukla, Maexxna, TheBeast)


class TimberWolf(MinionCard):
    def __init__(self):
        super().__init__("Timber Wolf", 1, CHARACTER_CLASS.HUNTER, CARD_RARITY.FREE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(1, 1, auras=[Aura(ChangeAttack(1), MinionSelector(MinionIsType(MINION_TYPE.BEAST)))])


class SavannahHighmane(MinionCard):
    def __init__(self):
        super().__init__("Savannah Highmane", 6, CHARACTER_CLASS.HUNTER, CARD_RARITY.RARE, MINION_TYPE.BEAST)

    def create_minion(self, player):
        def summon_hyenas(m):
            class Hyena(MinionCard):
                def __init__(self):
                    super().__init__("Hyena", 2, CHARACTER_CLASS.HUNTER, CARD_RARITY.SPECIAL)

                def create_minion(self, player):
                    return Minion(2, 2, MINION_TYPE.BEAST)

            Hyena().summon(m.player, m.game, m.index)
            Hyena().summon(m.player, m.game, m.index)

        return Minion(6, 5, deathrattle=summon_hyenas)


class Houndmaster(MinionCard):
    def __init__(self):
        super().__init__("Houndmaster", 4, CHARACTER_CLASS.HUNTER, CARD_RARITY.FREE, MINION_TYPE.NONE,
                         hearthbreaker.targeting.find_friendly_minion_battlecry_target,
                         lambda m: m.card.minion_type is MINION_TYPE.BEAST)

    def create_minion(self, player):
        def buff_beast(m):
            if self.target is not None:
                self.target.increase_health(2)
                self.target.change_attack(2)
                self.target.taunt = True

        return Minion(4, 3, battlecry=buff_beast)


class KingKrush(MinionCard):
    def __init__(self):
        super().__init__("King Krush", 9, CHARACTER_CLASS.HUNTER, CARD_RARITY.LEGENDARY, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(8, 8, charge=True)


class StarvingBuzzard(MinionCard):
    def __init__(self):
        super().__init__("Starving Buzzard", 5, CHARACTER_CLASS.HUNTER, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(3, 2, effects=[NewEffect(MinionPlaced(MinionIsType(MINION_TYPE.BEAST)), Draw(), Owner())])


class TundraRhino(MinionCard):
    def __init__(self):
        super().__init__("Tundra Rhino", 5, CHARACTER_CLASS.HUNTER, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 5, charge=True,
                      auras=[Aura(Charge(), MinionSelector(MinionIsType(MINION_TYPE.BEAST)))])


class ScavengingHyena(MinionCard):
    def __init__(self):
        super().__init__("Scavenging Hyena", 2, CHARACTER_CLASS.HUNTER, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        return Minion(2, 2, effects=[NewEffect(MinionDied(MinionIsType(MINION_TYPE.BEAST)), ChangeAttack(2), Self()),
                                     NewEffect(MinionDied(MinionIsType(MINION_TYPE.BEAST)), ChangeHealth(1), Self())])


class Webspinner(MinionCard):
    def __init__(self):
        super().__init__("Webspinner", 1, CHARACTER_CLASS.HUNTER, CARD_RARITY.COMMON, MINION_TYPE.BEAST)

    def create_minion(self, player):
        def add_beast_to_hand(minion):
            beast_cards = [RiverCrocolisk, BloodfenRaptor, OasisSnapjaw, StonetuskBoar, CoreHound, DireWolfAlpha,
                           HauntedCreeper, IronbeakOwl, IronfurGrizzly, JunglePanther, SilverbackPatriarch,
                           StranglethornTiger, YoungDragonhawk, AngryChicken, EmperorCobra, StampedingKodo,
                           CaptainsParrot, HungryCrab, KingMukla, Maexxna, TimberWolf, ScavengingHyena, StarvingBuzzard,
                           TundraRhino, Webspinner, SavannahHighmane, KingKrush, TheBeast]
            card = minion.game.random_choice(beast_cards)
            if len(minion.player.hand) < 10:
                minion.player.hand.append(card())

        return Minion(1, 1, deathrattle=add_beast_to_hand)
