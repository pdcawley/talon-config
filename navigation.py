from talon.voice import Key, press, Str, Context
from .repeater import ordinals

ctx = Context('navigation')

keymap = {
    '(forward [word] | nord)': Key('alt-right'),
    '(backward | hard | bard)': Key('alt-left'),
    '(barend | brend)':  Key('alt-left alt-right'),
    '(dumbble | lurd)': Key('alt-backspace'),
    '(D-word | kimble)': Key('alt-d'),
    'slurp': Key('ctrl-k'),
    'pup': Key('pgup'),
    'pown': Key('pgdown'),

    '(yoll | yawl)': Key('ctrl-e'),


    'foo': 'foo'
}

ctx.keymap(keymap);
