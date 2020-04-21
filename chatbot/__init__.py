from collections import deque, ChainMap
from itertools import chain
import json

ask_string = lambda x: input(x)
ask_int = lambda x: int(input(x))

chatflows_states = {}
# questions, star


def is_hashable(v):
    try:
        hash(v)
    except TypeError:
        return False
    return True


def id_of_step_name(step_name):
    return int(step_name.split("step_")[1])


class Chatflow:
    def __init__(self):
        import uuid

        self.id = str(uuid.uuid4())
        self._state = {}
        self._current_step_name = "step_0"

    @property
    def current_step_id(self):
        # add sentinel for None
        return id_of_step_name(self._current_step_name)

    @property
    def _next_step_name(self):
        return f"step_{self.current_step_id+1}"

    @property
    def _prev_step_name(self):
        return f"step_{self.current_step_id-1}"

    def _execute_step(self, _step_name):
        step_fn = getattr(self, _step_name)
        prev_states = []
        for prevstep, state in self._state.items():
            prevstep_id = id_of_step_name(prevstep)
            if prevstep_id >= self.current_step_id:
                break

            prev_states.append(state)

        flattened_states = ChainMap(prev_states)
        # print("previous state: ", flattened_states)
        _locals_of_step = step_fn(flattened_states)

        hashable_locals_of_step = {k: v for k, v in _locals_of_step.items() if is_hashable(v)}

        hashable_locals_of_step.pop("self", None)  # make sure we don't have self not hashable.
        self._state[_step_name] = hashable_locals_of_step

        chatflows_states[self.id] = self._state
        # print(chatflows_states)

    def go_next(self):
        res = self._execute_step(self._next_step_name)
        self._current_step_name = self._next_step_name
        return res

    def go_prev(self):
        res = self._execute_step(self._prev_step_name)
        self._current_step_name = self._prev_step_name
        return res

    def interact(self, m):
        if m["action"] == "next":
            return self.go_next()

        elif m["action"] == "prev":
            return self.go_prev()

    def start(self, start_step_name=None):
        start_step_name = start_step_name or "step_1"
        steps_funs = [step for step in dir(self) if step.startswith("step_")]
        # steps_funs should be ordered.
        for step_fun_name in steps_funs:
            current_step_id = int(step_fun_name.split("step_")[1])
            if step_fun_name < start_step_name:
                continue
            step_fn = getattr(self, step_fun_name)
            prev_states = []
            for prevstep, state in self._state.items():
                prevstep_id = int(prevstep.split("step_")[1])
                if prevstep_id >= current_step_id:
                    break

                prev_states.append(state)

            flattened_states = ChainMap(prev_states)
            # print("previous state: ", flattened_states)
            _locals_of_step = step_fn(flattened_states)

            hashable_locals_of_step = {k: v for k, v in _locals_of_step.items() if is_hashable(v)}

            hashable_locals_of_step.pop("self", None)  # make sure we don't have self not hashable.
            self._state[step_fun_name] = hashable_locals_of_step

            chatflows_states[self.id] = self._state
            # print(chatflows_states)
