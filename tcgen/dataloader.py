import os
import json
from tcgen import constants


def truncate_string(text, length):
    for i in range(length, 0, -1):
        if text[i] == " ":
            return text[:i], text[i+1:]
    return text[:length], text[length:]

class CardData(object):
    
    EFFECT_MAX_CHAR = 68
    FLAVOR_MAX_CHAR = 55

    def __init__(self, data_dict, faction, layout):
        self.name = data_dict["name"]
        self.faction = faction
        self.layout = layout
        self.effect = data_dict["effect"]
        self.value = data_dict.get("value", {})
        self.flavor = data_dict.get("flavor", "")
        self.count = data_dict.get("count", 1)

        self.effect_strings = self.get_effect_strings()
        self.flavor_strings = self.get_flavor_strings()

    @property
    def image(self):
        prefix = "img/{}".format(
            self.name.lower().replace(" ", "")
        )

        for file_format in (".jpg", ".png", ".gif"):
            if os.path.exists(prefix + file_format):
                return prefix + file_format
        
        return None

    def get_value_strings(self):
        top = ""
        bottom = []

        for k, v in self.value.items():
            if k == constants.TOP_VALUE:
                top = str(v)
            else:
                bottom.append("| {}: {} |".format(str(k).upper(), str(v)))
        
        return top, bottom

    def get_effect_strings(self):
        string_list = []
        for effect_type in self.effect:
            effect_string = self.effect.get(effect_type)
            if effect_string is None: continue
            effect_string = "[{}] {}".format(effect_type.upper(), effect_string)

            while len(effect_string) > CardData.EFFECT_MAX_CHAR:
                head, tail = truncate_string(effect_string,
                                             CardData.EFFECT_MAX_CHAR)
                string_list.append(head)
                effect_string = tail
            string_list.append(effect_string)
            string_list.append("")
        return string_list

    def get_flavor_strings(self):
        string_list = []
        flavor = self.flavor
        while len(flavor) > CardData.FLAVOR_MAX_CHAR:
            head, tail = truncate_string(flavor, CardData.FLAVOR_MAX_CHAR)
            string_list.append(head)
            flavor = tail
        string_list.append(flavor)
        return string_list


class BossData(CardData):
    def __init__(self, data_dict, faction, layout):
        self.summon = data_dict["summon"]
        self.returns = data_dict["return"]
        super(BossData, self).__init__(data_dict, faction, layout)

    def get_effect_strings(self):
        effect_strings = super(BossData, self).get_effect_strings()

        summon_strings = []
        summon = "[SUMMON] " + self.summon
        while len(summon) > CardData.EFFECT_MAX_CHAR:
            head, tail = truncate_string(summon, CardData.EFFECT_MAX_CHAR)
            summon_strings.append(head)
            summon = tail
        summon_strings.append(summon)
        summon_strings.append("")
        
        return_strings = []
        returns = "[RETURN] " + self.returns
        while len(returns) > CardData.EFFECT_MAX_CHAR:
            head, tail = truncate_string(returns, CardData.EFFECT_MAX_CHAR)
            return_strings.append(head)
            returns = tail
        return_strings.append(returns)
        return_strings.append("")

        return summon_strings + return_strings + effect_strings


class FactionData:
    def __init__(self, data_dict):
        self.faction_name = data_dict["faction"]
        self.layout = data_dict["layout"]
        self.cards = [CardData(cardmeta, self.faction_name, self.layout)
                      for cardmeta in data_dict["cards"]]
        if "boss" in data_dict:
            self.boss = BossData(data_dict["boss"], self.faction_name, self.layout)
        else:
            self.boss = None

    @staticmethod
    def load_data(faction):
        with open("data/{}".format(faction), "r") as factionfile:
            faction_data = json.load(factionfile)
            faction = FactionData(faction_data)
        return faction

    def get_card_instances(self):
        """
        Returns a list of CardData object, multiplied by
        their count.
        """
        card_instances = []
        for card in self.cards:
            card_instances += ([card] * card.count)
        return card_instances
