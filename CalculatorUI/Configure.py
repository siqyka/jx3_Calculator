import tools

CONFPATH='../Configuration/GameConf.ini'
PRO_ATT={
    "701":"力道",
    "702":"根骨"
    
}
class GameConf():
    def __init__(self) -> None:
        self.pro=tools.Conf(CONFPATH).redaConf('professional','pro')
    
    def getPro(self,is_all=False):
        proName=tools.CommonHelper.readDate('../CalculatorData/proID.json')
        if is_all:
            return proName[self.pro]
        return (proName[self.pro]['pro'],proName[self.pro]['name'])

        
    def getAttributeName(self):
        
        attributeName = ["最大气血值", "基础攻击", "最终攻击", PRO_ATT[self.pro], "武器伤害", "会心几率", "会心效果",
                     "破防等级", "破防率", "破招值", "无双值", "无双率", "加速", "加速率", "加速档位", "装备分数"]
        return attributeName
    
    def getCombatOptions(self):
        all=tools.CommonHelper.readDate('../CalculatorData/buff/combatOptions.json')
        pro=self.getPro()[0]
        return all[pro]['combatOptionsL']
    
    
    def getRarabooks(self):
        all=tools.CommonHelper.readDate('../CalculatorData/raraBook/raraBooks.json')
        pro=self.getPro()[0]
        return all[pro] 
   

    def getBuffs(self):
        all=tools.CommonHelper.readDate('../CalculatorData/buff/buffs.json')
        return all.values()

    def getQixue(self):
        pro=self.getPro()
        # all=tools.CommonHelper.readDate('../CalculatorData/qiXue/{}.json'.format(pro))
        all=tools.CommonHelper.readDate('../CalculatorData/qiXue/all.json')
        return all[pro[1]]


class MainWindowConf():
    windowIcon = "../artResources/defaultLattice/10026.png"
    windowTitle = "天策DPS计算器"


