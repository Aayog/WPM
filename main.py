import curses
from curses import wrapper
from random import choice
import time


prompts = [
    "The quick brown fox jumps over the lazy dog.",
    "A towering genius may exist in a bricklayer, poet, or coal miner.",
    "Jaded zombies acted quaintly but kept driving their oxen forward.",
    "How vexingly quick daft zebras jump!",
    "Amazingly few discotheques provide jukeboxes.",
    "We promptly judged antique onyx buckles for prizes.",
    "Crazy Fredrick bought many very exquisite opal jewels.",
    "The five boxing wizards jump quickly.",
    "Pack my box with five dozen liquor jugs.",
    "We promptly served the cooling fried chicken.",
    "My faxed joke won a pager in the cable TV quiz show.",
    "Amazingly few discotheques provide jukeboxes.",
    "The quick brown dog jumps over the lazy fox.",
    "Sphinx of black quartz, judge my vow.",
    "How razorback-jumping frogs can level six piqued gymnasts!",
    "The five boxing wizards jump quickly.",
    "Jaded zombies acted quaintly but kept driving their oxen forward.",
    "The quick onyx goblin jumps over the lazy dwarf.",
    "We promptly judged antique onyx buckles for prizes.",
    "Crazy Fredrick bought many very exquisite opal jewels."
]

def typing_err_ok_logic(stdcsr, picked):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    i = 0
    y = 1
    x = 10
    start_time = 0
    end_time = 0
    typed = ""
    while True:
        if i >= len(picked):
            break
        key = stdcsr.getkey()
        if start_time == 0:
            start_time = time.time()
        if ord(key) == 127:
            i -= 1
            typed = typed[:-1]
            if i < 0:
                i = 0
                continue
            stdcsr.addstr(y, x + i, picked[i], curses.color_pair(3))
            curses.setsyx(y, x + i -1)
            i -= 1
        elif key == picked[i]:
            stdcsr.addstr(y, x + i, key, curses.color_pair(1))
        else:
            stdcsr.addstr(y, x + i, key, curses.color_pair(2))
        typed += key
        i += 1
        if i <= 0:
            i = 0
    end_time = time.time()
    error = calculate_error_rate(typed, picked)
    return (end_time - start_time), error

def calculate_error_rate(typed, picked):
    error_count = 0
    for t, p in zip(typed, picked):
        if t != p:
            error_count += 1
    error_rate = (error_count / len(picked)) * 100
    return error_rate

def start_screen(stdcsr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    max_y, max_x = stdcsr.getmaxyx()
    y = max_y // 2  # Center the text vertically
    x = max_x // 2 - len("Welcome to the Typing Game") // 2  # Center the text horizontally
    stdcsr.addstr(y, x, "Welcome to the Typing Game", curses.color_pair(1))

    y += 2
    x = max_x // 2 - len("Let's find out your WPM") // 2
    stdcsr.addstr(y, x, "Let's find out your WPM", curses.color_pair(1))

    y += 2
    x = max_x // 2 - len("Press any key to Continue") // 2
    stdcsr.addstr(y, x, "Press any key to Continue", curses.color_pair(1))
    stdcsr.getkey()

def main(stdcsr):
    start_screen(stdcsr)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    picked = choice(prompts)
    stdcsr.clear()
    stdcsr.addstr(1, 10, picked, curses.color_pair(3))
    stdcsr.refresh()
    curses.curs_set(0)  
    delta_time, err = typing_err_ok_logic(stdcsr, picked)
    stdcsr.clear()
    your_time_msg = f"Your time is {delta_time:.2f} seconds"
    wpm = len(picked.split(" ")) / (delta_time/60)
    max_y, max_x = stdcsr.getmaxyx()
    y = max_y // 2  # Center the text vertically
    x = max_x // 2 - len(your_time_msg) // 2  # Center the text horizontally
    stdcsr.addstr(y, x, your_time_msg, curses.color_pair(1))
    stdcsr.addstr(y + 3, x, f"WPM: {wpm}", curses.color_pair(1))
    stdcsr.addstr(y + 5, x, f"Error: {err:.2f}%", curses.color_pair(2))
    stdcsr.getkey()
    stdcsr.clear()
    stdcsr.addstr(y, x, "Press any key to exit", curses.color_pair(1))
    stdcsr.getkey()

if __name__ == "__main__":
    wrapper(main)
