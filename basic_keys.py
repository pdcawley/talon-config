from talon.voice import Context, Str, press
import string

#alpha_alt = 'air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip'.split()
alpha_alt  = 'ahff braav cai drum eck fay goff hoop ish jo keel lee mike noy odd pui queen red soi tay uni van wes plex yank zool'.split()


f_keys = {f'F {i}': f'f{i}' for i in range(1, 13)}
# arrows are separated because 'up' has a high false positive rate
arrows = ['left', 'right', 'up', 'down']
simple_keys = [
    'tab', 'escape', 'enter', 'space',
    'home', 'pageup', 'pagedown', 'end',
]
alternate_keys = {
    'delete': 'backspace',
    'chook': 'backspace',
    'del': 'delete',
    'forward delete': 'delete',
    'paa': 'space',
    'spa': 'space'
}
symbols = {
    #'back tick': '`', 'back quote': '`',
    'semi colon': ';', 'sem-col': ';', 'sem-coal': ';',
    'hyphen': '-', 'hive': '-', 'dash': '-',

    'back tick': '`', 'back quote': '`',
    'cam': ',',
    'dot': '.', 'period': '.',
    'quote': '"', 'dubquote': '"', 'double quote': '"',
    'sing': "'",
    'lack': '[',
    'rack': ']',
    'laip': '(',
    'rape': ')',
    'rye': ')',
    'lang': '<',
    'rang': '>',
    'lace': '{',
    'race': '}',
    'forward slash': '/', 'slash': '/',
    'backslash': '\\',
    'equal[s]': '=',
    'pipe': '|'
}
modifiers = {
    'command': 'cmd',
    'control': 'ctrl',
    'shift': 'shift',
    'meta': 'alt',
    'option': 'alt',
}

alphabet = dict(zip(alpha_alt, string.ascii_lowercase))
alphabet['aff'] = 'a'
alphabet['osc'] = 'o'
alphabet['echo'] = 'e'
alphabet['delta'] = 'd'
alphabet['lima'] = 'l'
alphabet['osh'] = 'o'
alphabet['rie'] = 'r'

digits = {str(i): str(i) for i in range(10)}
simple_keys = {k: k for k in simple_keys}
simple_keys['paa'] = 'space'
print(simple_keys)
arrows = {k: k for k in arrows}
keys = {}
keys.update(f_keys)
keys.update(simple_keys)
keys.update(alternate_keys)
keys.update(symbols)

# map alnum and keys separately so engine gives priority to letter/number repeats
keymap = keys.copy()
keymap.update(arrows)
keymap.update(alphabet)
keymap.update(digits)

def insert(s):
    Str(s)(None)

def get_modifiers(m):
    try:
        return [modifiers[mod] for mod in m['basic_keys.modifiers']]
    except KeyError:
        return []

def get_keys(m):
    groups = ['basic_keys.keys', 'basic_keys.arrows', 'basic_keys.digits', 'basic_keys.alphabet']
    for group in groups:
        try:
            return [keymap[k] for k in m[group]]
        except KeyError: pass
    return []

def uppercase_letters(m):
    insert(''.join(get_keys(m)).upper())

def press_keys(m):
    mods = get_modifiers(m)
    keys = get_keys(m)
    if mods:
        press('-'.join(mods + [keys[0]]))
        keys = keys[1:]
    for k in keys:
        press(k)

ctx = Context('basic_keys')
ctx.keymap({
    '(uppercase | ship) {basic_keys.alphabet}+ [(lowercase | sunk)]': uppercase_letters,
    '{basic_keys.modifiers}* {basic_keys.alphabet}+': press_keys,
    '{basic_keys.modifiers}* {basic_keys.digits}+': press_keys,
    '{basic_keys.modifiers}* {basic_keys.keys}+': press_keys,
    '(go | {basic_keys.modifiers}+) {basic_keys.arrows}+': press_keys,
})
ctx.set_list('alphabet', alphabet.keys())
ctx.set_list('arrows', arrows.keys())
ctx.set_list('digits', digits.keys())
ctx.set_list('keys', keys.keys())
ctx.set_list('modifiers', modifiers.keys())
