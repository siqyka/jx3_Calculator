import tools
import Configure


Position = {
    "01": "HAT",
    "02": "JACKET",
    "03": "BELT",
    "04": "SECONDARY_WEAPON",
    "05": "PRIMARY_WEAPON",
    "06": "WRIST",
    "07": "BOTTOMS",
    "08": "SHOES",
    "09": "NECKLACE",
    "10": "PENDANT",
    "11": "RING",
    "12": "RING",
}


class Cevents():
    def __init__(self):
        pass

    def dealM(self, m, s):
        i = m.find(s)
        if i == -1:
            m = m.replace("命中", "破招").replace("攻击", "").replace("全能", "会心破防加速")
        else:
            m = m[:i:].replace("命中", "破招").replace("攻击", "")
        return m

    def getMateriel(self, position):
        p = '../CalculatorData/materiel/{}.json'.format(Position[position])
        d = Configure.GameConf().getPro(True)
        # print(d)
        all_d = tools.CommonHelper.readDate(p)
        materiels = []
        # 返回名称，属性，品级
        for k in all_d['list']:
            if k['BelongSchool'] == "通用" and k["MagicKind"] == d['atb']:
                materiels.append({"ID": k['ID'], "MagicType": self.dealM(
                    k['MagicType'], "高级"), 'Level': k['Level'], 'Name': k['Name'],'_IconID': k['_IconID']})
            elif k['BelongSchool'] == "精简" and k["MagicKind"] == d['Belong']:
                materiels.append({"ID": k['ID'], "MagicType": self.dealM(
                    k['MagicType'], "高级"), 'Level': k['Level'], 'Name': k['Name'],'_IconID': k['_IconID']})
            elif k['BelongSchool'] == d['mp']:
                materiels.append({"ID": k['ID'], "MagicType": self.dealM(
                    k['MagicType'], "高级"), 'Level': k['Level'], 'Name': k['Name'],'_IconID': k['_IconID']})
        # print(materiels)
        return materiels

    def getAMateriel(self, id, position):
        p = '../CalculatorData/materiel/{}.json'.format(Position[position])
        all_d = tools.CommonHelper.readDate(p)
        for k in all_d['list']:
            if id == k['ID']:
                return k

    def getAMaterielHtml(self, id, position):
        attr_d = tools.CommonHelper.readDate(
            '../CalculatorData/materiel/attr.json')
        htmlStrH = '''<html><head><body>'''
        htmlStrL = '''</body></html>'''
        md = self.getAMateriel(id, position)
        Name = md['Name']
        # 外功基础防御
        Base1 = md['Base1Min']
        # 内功基础防御
        Base2 = md['Base2Min']
        baseAttr = ['atAgilityBase', 'atSpunkBase',
                    'atStrengthBase', 'atSpiritBase', 'atVitalityBase']
        # 基础属性
        baseA = []
        # 其他属性
        otherA = []
        # 镶嵌
        inlay = []
        # 最大精炼等级
        MaxStrengthLevel = md['MaxStrengthLevel']
        # 品质
        Level = md['Level']
        # 装备分数
        # ？？？
        # 特性
        txattr = ['atSetEquipmentRecipe', 'atSkillEventHandler']
        txA = []
        yztx = md['_SkillDesc']
        for m in range(1, 13):
            ind = '_Magic{}Type'.format(str(m))
            if md[ind]:
                if md[ind]['attr'][0] in baseAttr:
                    baseA.append({md[ind]['attr'][0]: md[ind]['attr'][1]})
                elif md[ind]['attr'][0] in txattr:
                    txA.append(md[ind]['label'])
                else:
                    otherA.append({md[ind]['attr'][0]: md[ind]['attr'][1]})
        for d in range(1, 4):
            ind = '_DiamondAttributeID{}'.format(str(d))
            if md[ind]:
                inlay.append(md[ind][0])
        # 名称
        hs1 = '''<div style="font:15px Microsoft YaHei; color:rgb(233, 45, 234);" >{}</div>'''.format(
            Name)

        hs2 = '''<div style="font:15px Microsoft YaHei; color:rgb(255, 255, 255);" >外功防御等级提高{}</div>'''.format(
            Base1)
        hs3 = '''<div style="font:15px Microsoft YaHei; color:rgb(255, 255, 255);" >内功防御等级提高{}</div>'''.format(
            Base2)
        # 基础属性
        hs4 = ''
        if baseA:
            for ba in baseA:
                lb = list(ba.items())[0]
                hs4 += '''<div style="font:15px Microsoft YaHei; color:rgb(255, 255, 255);" >{}+{}</div>'''.format(
                    attr_d[lb[0]], lb[1])
        # 装备属性
        hs5 = ''
        if otherA:
            for oa in otherA:
                lb = list(oa.items())[0]
                if "攻击" in attr_d[lb[0]]:
                    hs5 += '''<div style="font:15px Microsoft YaHei; color:rgb(0, 184, 53);" >{}提高{}</div>'''.format(
                        attr_d[lb[0]], lb[1])
                else:
                    hs5 += '''<div style="font:15px Microsoft YaHei; color:rgb(0, 184, 53);" >{}等级提高{}</div>'''.format(
                        attr_d[lb[0]], lb[1])
        # 特效
        hs6 = ''
        if txA:
            rr = ['<text>text=\"', '<Text>text=\"',
                  '\" font=101 </text>', '\\']
            for ta in txA:
                for r in rr:
                    ta = ta.replace(r, "")
                hs6 += '''<div style="font:15px Microsoft YaHei; color:rgb(255,134,22);max-width: 10px;" >{}</div>'''.format(
                    ta)
        # 镶嵌
        hs7 = ''
        if inlay:
            for il in inlay:
                # lb=list(oa.items())[0]
                hs7 += '''<div style="font:15px Microsoft YaHei; color:rgb(0, 184, 53);" >◻镶嵌孔：{}</div>'''.format(
                    attr_d[il])
        # 特效
        yz = ''
        if yztx:
            yz = '''<br></br><div style="font:15px Microsoft YaHei; color:rgb(0, 184, 53);" >{}</div>'''.format(
                yztx[yztx.find("使用"):yztx.find("。")+1])
        # 品质
        hs8 = '''<br></br><div style="font:15px Microsoft YaHei; color:rgb(201, 201, 17);" >品质等级 {}</div>'''.format(
            Level)
        # cw特殊处理
        if position == '05' or position == '04':
            is_o = md['BelongMap']
            if is_o == '橙武':
                hs1 = '''<div style="font:15px Microsoft YaHei; color:rgb(255,134,22);" >{}</div>'''.format(
                    Name)
            hs2 = '''<div style="font:15px Microsoft YaHei; color:rgb(255, 255, 255);" >近身伤害提高 {} - {}</div>'''.format(
                Base1, Base2)
            hs3 = ""

        htmlall = htmlStrH+hs1+hs2+hs3+hs4+hs5+hs6+hs7+yz+hs8+htmlStrL
        return htmlall

    def getFM(self,position="01"):
        position="01"
        pd = '../CalculatorData/fm/{}_D.json'.format(Position[position])
        px='../CalculatorData/fm/{}_X.json'.format(Position[position])
        all_pd = tools.CommonHelper.readDate(pd)
        all_px = tools.CommonHelper.readDate(px)
        pds = []
        pxs=[]
        for p in all_pd:
            pds.append({"ID":p["ID"],"Name":p["Name"]})
        
        for x in all_px:
            if x["Name"].find("）")!=-1:
                name=x["Name"].replace("）", str(x["Attribute1Value1"])+"点）")
                pxs.append({"ID":p["ID"],"Name":name})
            else:
                pxs.append({"ID":p["ID"],"Name":x["Name"]+"（"+str(x["Attribute1Value1"])+"点）"})
        return (pds,pxs)
a = Cevents()
a.getFM('01')
