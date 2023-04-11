from mitmproxy.http import HTTPFlow
from addons import ArkInterceptor
from model.troopBuilder import troopBuilder
import json

class graduateChars(ArkInterceptor):
    '''
        Require: CharsEssential,BattleEssential
    '''
    def __init__(self):
        self.e = True
        self.info("Loading success")

    def executable(self):
        return self.e

    @ArkInterceptor.checkExecutable
    def response(self, flow: HTTPFlow):
        if self.inServersList(flow.request.host) and flow.request.path.startswith("/account/syncData"):
            self.info("Receive response")
            data = json.loads(flow.response.get_text())
            for key,char in self.tBuilder.chars.items():
                self.info("Upgrade: %s-%s" %(key,char["charId"]))
                self.tBuilder.chars[key] = self.cBuilder.graduate(self.tBuilder.chars[key])
            data["user"]["troop"] = self.tBuilder.dump()
            flow.response.set_text(json.dumps(data))
            self.info("Complete")
            self.e = False

#master.addons.add(graduateChars())