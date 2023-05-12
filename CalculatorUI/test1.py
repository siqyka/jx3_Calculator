from typing import List, Dict
import json
from json import JSONEncoder


class PZEquipSnapshot:

    id: str
    stone: object
    enchant: object
    enhance: object
    strength: int = 0
    embedding: List[int]

    def __init__(self, id: str, stone: object, enchant: object, enhance: object, strength: int, embedding: List[int]):
        self.id = id
        self.stone = stone
        self.enchant = enchant
        self.enhance = enhance
        self.strength = strength
        self.embedding = embedding


class JBPZPanel:
    Agility: float
    Spirit: float
    Spunk: float
    Strength: float
    StrainPercent: float
    HastePercent: float
    SurplusValue: float
    MaxHealth: float
    ToughnessDefCriticalPercent: float
    DecriticalDamagePercent: float
    MeleeWeaponAttackSpeed: float
    MeleeWeaponDamage: float
    MeleeWeaponDamageRand: float

    EquipList: Dict[str, PZEquipSnapshot]
    Title: str

    @classmethod
    def from_json(cls, s: str):
        res = cls()
        d = json.loads(s)
        res.__dict__.update(d)
        if "EquipList" in d:
            equiplist = d["EquipList"]
            res.EquipList = {k: PZEquipSnapshot(**v) for k, v in equiplist.items()}
        else:
            res.EquipList = {}
        return res


class JBPZPanelEncoder(JSONEncoder):
    def default(self, o) -> dict:
        return o.__dict__


if __name__ == '__main__':
    sample = '''
    {"Vitality":34889,"Agility":41,"Spirit":41,"Spunk":41,"Strength":7318,
"PhysicsAttackPowerBase":20292,"PhysicsAttackPower":30904,"PhysicsCriticalStrikeRate":0.1854205221151706,"PhysicsCriticalDamagePowerPercent":1.7993571396120123,"PhysicsOvercomePercent":0.3839613342236637,
"StrainPercent":0.3225068180993744,"HastePercent":0.0074934898363714095,"SurplusValue":6413,
"MaxHealth":493241,"PhysicsShieldPercent":0.061682128156294154,"LunarShieldPercent":0.05403183576484102,"ToughnessDefCriticalPercent":0,"DecriticalDamagePercent":0.07,
"MeleeWeaponAttackSpeed":16,"MeleeWeaponDamage":1550,"MeleeWeaponDamageRand":1034,
"EquipList":{"HAT":{"id":"7_90835","stone":"","enchant":11684,"enhance":11531,"strength":6,"embedding":[6,6]},
"BELT":{"id":"7_90777","stone":"","enchant":11680,"enhance":"","strength":6,"embedding":[6,6]},
"SHOES":{"id":"7_90806","stone":"","enchant":11681,"enhance":11586,"strength":6,"embedding":[6,6]},
"WRIST":{"id":"7_90918","stone":"","enchant":11682,"enhance":11579,"strength":6,"embedding":[6,6]},
"JACKET":{"id":"7_90864","stone":"","enchant":11683,"enhance":"","strength":6,"embedding":[6,6]},
"RING_1":{"id":"8_34443","stone":"","enchant":"","enhance":11660,"strength":6,"embedding":[]},
"RING_2":{"id":"8_34303","stone":"","enchant":"","enhance":11660,"strength":6,"embedding":[]},
"BOTTOMS":{"id":"7_91333","stone":"","enchant":"","enhance":11524,"strength":6,"embedding":[6,6]},
"PENDANT":{"id":"8_34297","stone":"","enchant":"","enhance":11654,"strength":6,"embedding":[6]},
"NECKLACE":{"id":"8_34291","stone":"","enchant":"","enhance":11652,"strength":6,"embedding":[6]},
"PRIMARY_WEAPON":{"id":"6_33463","stone":561,"enchant":"","enhance":11517,"strength":6,"embedding":[6,6,6]},
"SECONDARY_WEAPON":{"id":"6_32774","stone":"","enchant":"","enhance":11669,"strength":6,"embedding":[6]}},
"Title":"展锋毕业"}
    '''
    res = JBPZPanel.from_json(sample)
    jsonstr = json.dumps(res, cls = JBPZPanelEncoder)
    print(jsonstr)
    
