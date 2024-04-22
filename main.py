import curses
from curses import wrapper
import curses.ascii
from random import choice
import time


prompts = [
"The quick brown fox jumps over the lazy dog in the lush green meadow on a warm summer day.",
"A towering genius may exist in a bricklayer, poet, or coal miner, hidden away from the world, waiting to be discovered.",
"Jaded zombies acted quaintly but kept driving their oxen forward, trudging through the desolate wasteland in search of brains.",
"How vexingly quick daft zebras jump! Their agility and speed are truly a sight to behold in the wild African savanna.",
"Amazingly few discotheques provide jukeboxes these days, a sad reminder of the fading glory of the disco era.",
"We promptly judged antique onyx buckles for prizes at the prestigious gemstone exhibition, admiring their timeless beauty.",
"Crazy Fredrick bought many very exquisite opal jewels from the eccentric jeweler, adding to his already impressive collection.",
"The five boxing wizards jump quickly, dodging spells and counterspells in their epic duel of magical might.",
"Pack my box with five dozen liquor jugs carefully, ensuring they don't break during the long journey ahead.",
"We promptly served the cooling fried chicken to the hungry crowd, its aroma wafting through the air enticingly.",
"My faxed joke won a pager in the cable TV quiz show, a relic of the past that brought back nostalgic memories.",
"Amazingly few discotheques provide jukeboxes nowadays, but those that do offer a unique and retro experience.",
"The quick brown dog jumps over the lazy fox, asserting its dominance in the backyard territory.",
"Sphinx of black quartz, judge my vow to unravel your ancient riddles and unlock the secrets of the ages.",
"How razorback-jumping frogs can level six piqued gymnasts! A truly remarkable feat of amphibian agility.",
"The five boxing wizards jump quickly, their robes swirling as they exchange lightning-fast blows in the arena.",
"Jaded zombies acted quaintly but kept driving their oxen forward, driven by an insatiable hunger for living flesh.",
"The quick onyx goblin jumps over the lazy dwarf, snatching the glittering treasure from under his nose.",
"We promptly judged antique onyx buckles for prizes, scrutinizing each intricate detail and admiring the artistry.",
"Crazy Fredrick bought many very exquisite opal jewels, each one more breathtakingly beautiful than the last."
]
def is_key_backspace(key):
    return key in ("KEY_BACKSPACE", chr(127), chr(8), "\b", "\x08", "\x7f") 

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
        if is_key_backspace(key):
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

def end_screen(stdcsr, x, y):
    stdcsr.addstr(y, x, "Press 'r' key to to play again", curses.color_pair(1))
    stdcsr.addstr(y + 2, x, "Press any to key to exit", curses.color_pair(1))
    k = stdcsr.getkey()
    if k == "r":
        main(stdcsr)

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
    end_screen(stdcsr, x, y)

if __name__ == "__main__":
    wrapper(main)
