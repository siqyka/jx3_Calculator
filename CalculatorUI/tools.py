# def append_Style(y,a):
#     ns=y[:y.rfind('}')]+a+'}' if y[y.rfind('}')-1]==';' else y[:y.rfind('}')]+';'+a+'}'
#     return ns
import os
import json
import configparser

class CommonHelper:
    def __init__(self):
        pass
 
    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()
        
    @staticmethod
    def readQsss(filepath):
        # with open(filepath, 'r') as f:
        #     return f.read()
        res = []
        strQss=''
        for (_, _, file_names) in os.walk(filepath):
            res=[x for x in file_names if x[-3:].lower()=='qss']
        for file in res:
            ff=os.path.join(filepath,file)
            with open(ff, 'r') as f:
                strQss+=f.read()
        return strQss
    
    @staticmethod
    def readDate(filepath):
        with open(filepath, 'r',encoding='utf-8') as f:
            return json.loads(f.read())
        
class Conf():
    def __init__(self,filepath='../Configuration/GameConf.ini') -> None:
        self.config = configparser.ConfigParser() # 类实例化

        self.path = filepath
        self.config.read(self.path)
        
    def redConfs(self,s):
       return self.config.items(s)
   
    def redaConf(self,s,k):
       return self.config.get(s,k)
   
    def writeConf(self,s,k,v):
        self.config.set(s,k,v)
        with open(self.path, 'w') as f:
            self.config.write(f)
        
        
if __name__=="__main__": 
    a=Conf('../Configuration/GameConf.ini')
    c=a.writeConf('professional','pro','701')
    b=CommonHelper.readDate('../CalculatorData/qiXue/all.json')
    print(b.keys())
    # print(c)
