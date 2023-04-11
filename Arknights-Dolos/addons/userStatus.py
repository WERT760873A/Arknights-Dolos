from mitmproxy.http import HTTPFlow
from addons import ArkInterceptor
import json

class userInfo(ArkInterceptor):
    mapper = {"nickName":lambda x:x.nickName,
              "nickNumber":lambda x:x.nickNumber,
              "level": lambda x:x.level,
              "exp":lambda x:x.exp,
              "resume":lambda x:x.resume,
              "uid":lambda x:x.uid}
    types = {"level":lambda x:int(x),
             "exp":lambda x:int(x)}

    def __init__(self):
        self.nickName,self.nickNumber,self.level,self.exp = [None] *4
        self.resume = None
        self.uid = None
        self.info("Loading success")

    @classmethod
    # 能用的只有nickname, nicknumber, level 和exp
    def init(cls,name,nums,level,exp):
        self = cls()
        self.nickName, self.nickNumber, self.level, self.exp = name,nums,level,exp
        #self.resume = resume
        # self.uid = uid
        return self


    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            for key,value in self.mapper.items():
                val = value(self)
                if val is not None:
                    self.info("Change %s: %s -> %s" %(key,data["user"]["status"][key],val))
                    if (key in self.types.keys()):
                        data["user"]["status"][key] = self.types[key](val)
                    else:
                        data["user"]["status"][key] = val
            flow.response.set_text(json.dumps(data))
            self.info("Complete")


class userData(ArkInterceptor):
    mapper = {"ap":lambda x:x.ap,
              "maxAp":lambda x:x.maxAp,
              "androidDiamond": lambda x:x.diamond,
              "iosDiamond":lambda x:x.diamond,
              "diamondShard":lambda x:x.diamondShard,
              "gold":lambda x:x.gold
              }
    types = {"ap":lambda x:int(x),
              "maxAp":lambda x:int(x),
              "androidDiamond": lambda x:int(x),
              "iosDiamond":lambda x:int(x),
              "diamondShard":lambda x:int(x),
              "gold":lambda x:int(x)
              }

    def __init__(self):
        self.ap,self.maxAp,self.diamond,self.diamondShard,self.gold = [None] *5
        self.info("Loading success")

    @classmethod
    # 能用的只有nickname, nicknumber, level 和exp
    def init(cls,ap,maxAp,diamond,diamondShard,gold):
        self = cls()
        self.ap,self.maxAp,self.diamond,self.diamondShard,self.gold = ap,maxAp,diamond,diamondShard,gold
        return self

    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            for key,value in self.mapper.items():
                val = value(self)
                if val is not None:
                    self.info("Change %s: %s -> %s" %(key,data["user"]["status"][key],val))
                    if (key in self.types.keys()):
                        data["user"]["status"][key] = self.types[key](val)
                    else:
                        data["user"]["status"][key] = val
            flow.response.set_text(json.dumps(data))
            self.info("Complete")

#
#info = userInfo.init("Rua牛","0000",120,0)
#data = userData.init(999,999,1919810,114514,6666666)

# master.addons.add(info)
# master.addons.add(data)