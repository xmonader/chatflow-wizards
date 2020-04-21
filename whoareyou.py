
from chatbot import Chatflow
from collections import deque, ChainMap
from itertools import chain
import json

ask_string = lambda x: input(x)
ask_int = lambda x: int(input(x))

chatflows_states = {}


class WhoAreYouChatflow(Chatflow):
    def step_1(self, prev_state):
        print(prev_state)
        name = ask_string("your name? ")
        print(f"hello,  {name}")
        return locals()

    def step_2(self, prev_state):
        print(prev_state)
        age = ask_int("your age? ")
        print(f"{age} !! that's old!!")
        return locals()

    def step_3(self, prev_state):
        print(prev_state)
        fav_club = ask_string("fav club? ")
        print(f"I like {fav_club} too!")
        return locals()


if __name__ == "__main__":
    # whoareyou_chatflow = WhoAreYouChatflow()
    # whoareyou_chatflow_id = whoareyou_chatflow.id
    # whoareyou_chatflow.start()

    # print("done, now will continue from step_2")
    # whoareyou_chatflow.start("step_2")

    # print("done, now will continue from step_3")
    # whoareyou_chatflow.start("step_3")

    whoareyou_chatflow2 = WhoAreYouChatflow()
    while True:
        act = input("next, prev, exit?")
        if act == "exit":
            print("bye bye..")
        else:
            whoareyou_chatflow2.interact({"action": act})
