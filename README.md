# chatflow-wizards

- for every method starts with step_ prefix we consider a step in the chatflow.
- each method receives prev_state a dict representing the previous info from previous steps
- each method returns locals (or a crafted state dict)
state stored in chatflows_states a Dict[ChatflowGuid][ChatState] and ChatState is Dict[step_name][step_state]

Example

```python

from chatbot import Chatflow


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


```

You can interact with next, prev actions like the following

```python
    whoareyou_chatflow2 = WhoAreYouChatflow()
    while True:
        act = input("next, prev, exit?")
        if act == "exit":
            print("bye bye..")
        else:
            whoareyou_chatflow2.interact({"action": act})

```
or you can start all of the chat steps using `.start()` or start at specific step using `.start(step_name)
`
```python
    whoareyou_chatflow = WhoAreYouChatflow()
    whoareyou_chatflow_id = whoareyou_chatflow.id
    whoareyou_chatflow.start()

    print("done, now will continue from step_2")
    whoareyou_chatflow.start("step_2")

    print("done, now will continue from step_3")
    whoareyou_chatflow.start("step_3")

```