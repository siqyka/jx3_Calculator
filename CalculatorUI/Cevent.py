import tools
import Configure


Position={
    "01":"HAT",
    "02":"JACKET"
}

class Cenents():
    def __init__(self):
        pass
    
    def getMateriel(self,position):
        p='../CalculatorData/materiel/{}.json'.format(Position[position])
        d=Configure.GameConf().getPro(True)
        print(d)
        all_d=tools.CommonHelper.readDate(p)
        materiel=[]
        for k in all_d['list']:
            if k['BelongSchool']=="通用" and k["MagicKind"]==d['atb']:
                materiel.append(k['ID'])
            elif k['BelongSchool']=="精简" and k["MagicKind"]==d['Belong']:
                materiel.append(k['ID'])
            elif k['BelongSchool']==d['mp']:
                materiel.append(k['ID'])
        return materiel
a=Cenents()
a.getMateriel("01")