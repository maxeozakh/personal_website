from typing import List, Union, Literal, TypedDict, Dict
import time
logs = []
def machine(tape: List) -> List:
    # "The symbol on the scanned square may be called the 'scanned symbol'
    # The 'scanned symbol' is the only one of which the machine is,
    # so to speak, 'directly aware'."
    awareness = 0

    state: Union[int, Literal["HALT"]] = 0

    class Action(TypedDict):
        move: List
        action: Literal["WRITE", "ERASE", "NONE"]
        value: Union[int, str, None]

    class Instruction(TypedDict):
        cond: Union[int, str, None]
        do: Action
        next_state: Union[int, Literal["HALT"]]

    instructions: Dict[int, List[Instruction]] = {
        0: [ {"cond": 0, "do": {"move": ["r", 0], "action": "NONE", "value": None}, "next_state": 2},
              {"cond": 1, "do": {"move": ["r", 0], "action": "ERASE", "value": None}, "next_state": 1} ],
        1: [ {"cond": None, "do": {"move": ["r", 0], "action": "WRITE", "value": "f"}, "next_state": 1},
              {"cond": "f", "do": {"move": ["r", 1], "action": "WRITE", "value": "l"}, "next_state": 1},
              {"cond": "l", "do": {"move": ["r", 1], "action": "WRITE", "value": "o"}, "next_state": 1},
              {"cond": "o", "do": {"move": ["r", 1], "action": "WRITE", "value": "w"}, "next_state": 1},
              {"cond": "w", "do": {"move": ["r", 1], "action": "WRITE", "value": "e"}, "next_state": 1},
              {"cond": "e", "do": {"move": ["r", 1], "action": "WRITE", "value": "r"}, "next_state": 1},
              {"cond": "r", "do": {"move": ["r", 1], "action": "NONE", "value": None}, "next_state": "HALT"} ],
        2: [ {"cond": 0, "do": {"move": ["r", 0], "action": "NONE", "value": None}, "next_state": "HALT"} ]
    }

    while state != "HALT":
        current_instructions = instructions[state]
        for instruction in current_instructions:
            condition = instruction["cond"]
            thing_to_do = instruction["do"]
            action = thing_to_do["action"]
            value = thing_to_do["value"]
            next_state = instruction["next_state"]
            move_to = thing_to_do["move"]

            tape_copy = tape[:]
            log = [
              state,
              condition,
              action,
              value,
              next_state,
              move_to,
              tape[awareness],
              tape_copy
            ]
            logs.append(log)
            if tape[awareness] != condition:
                continue


            [direction, step] = move_to
            if direction == "r":
                next_awareness = awareness + step
            else:
                next_awareness = awareness - step

            awareness = next_awareness

            if action == "WRITE":
                tape[awareness] = value
            elif action == "ERASE":
                tape[awareness] = None

            state = next_state
            break  # Exit the for-loop after executing the instruction

    logs.append([state, None, None, None, None, None, None, tape[:]])
    return tape

# I don't want to implement self-expanding data structure, since it's 
# feels less closer to the real machine, so Noneonneoneoe 
the_tape = [1, None, None, None, None, None]

machine(the_tape)


def visualizer(logs):
  print(f"""       
           ✶ the MACHINE state
           """)
  time.sleep(1.5)
  for i, log in enumerate(logs):
    [
      state,
      condition,
      action,
      value,
      next_state,
      move_to,
      awareness,
      tape
    ] = log

    timer_value = 0.1 if awareness != condition else .7
    timer_value2 = 0.1 if awareness != condition else .5

    thing = f"""    ┌────────────────────────────────────────────────────
    │    
    │    match?: {awareness == condition}   
    │    condition: {condition}               
    │    awareness: {awareness}   
    │    state: {state}                   
    │    action: {action}             
    │    value: {value}             
    │    move_to: {move_to}         
    │    next_state: {next_state}   
    │    
    │    tape: {tape}   
    │    
    └────────────────────────────────────────────"""
    print(thing)
    time.sleep(timer_value)
    if i != (len(logs) - 1):
      print(f"""                    ↓         """)
    time.sleep(timer_value2)

visualizer(logs)
