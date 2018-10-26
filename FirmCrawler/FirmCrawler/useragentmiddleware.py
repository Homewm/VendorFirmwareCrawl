# _*_ coding: utf-8 _*_
import random
from user_agents import agents
class randomUserAgentMiddleWare(object):
    def process_request(self,request,spider):
        agent = random.choice(agents)
        if agent:
            request.headers.setdefault('User-Agent',agent)