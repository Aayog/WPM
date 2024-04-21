import curses
from curses import wrapper
from random import choice
import time

prompts = [
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "The quick brown fox jumps over the lazy dog",
        "A touch typist does not need to move the sight between the keyboard (that is obscured with fingers and may be poorly lit) and other areas that require attention."
        "Typing speed is typically determined by how slow these weak keys are typed rather than how fast the remaining keys are typed."
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
    while True:
        if i >= len(picked):
            break
        key = stdcsr.getkey()
        if start_time == 0:
            start_time = time.time()
        if ord(key) == 127:
            i -= 1
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
        i += 1
        if i <= 0:
            i = 0
    end_time = time.time()
    return (end_time - start_time)

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
    delta_time = typing_err_ok_logic(stdcsr, picked)
    stdcsr.clear()
    your_time_msg = f"Your time is {delta_time:.2f} seconds"
    wpm = len(picked.split(" ")) / (delta_time/60)
    max_y, max_x = stdcsr.getmaxyx()
    y = max_y // 2  # Center the text vertically
    x = max_x // 2 - len(your_time_msg) // 2  # Center the text horizontally
    stdcsr.addstr(y, x, your_time_msg, curses.color_pair(1))
    stdcsr.addstr(y + 3, x, f"WPM: {wpm}", curses.color_pair(1))
    stdcsr.getkey()

if __name__ == "__main__":
    wrapper(main)
