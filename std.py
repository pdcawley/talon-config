
from talon.voice import Word, Context, Key, Rep, RepPhrase, Str, press
from talon import app, ctrl, clip, ui
from talon_init import TALON_HOME, TALON_PLUGINS, TALON_USER
import string

# cleans up some Dragon output from <dgndictation>
mapping = {
    'semicolon': ';',
    'new-line': '\n',
    'new-paragraph': '\n\n',
}
# used for auto-spacing
punctuation = set('.,-!?')

def parse_word(word):
    word = str(word).lstrip('\\').split('\\', 1)[0]
    word = mapping.get(word, word)
    return word

def join_words(words, sep=' '):
    out = ''
    for i, word in enumerate(words):
        if i > 0 and word not in punctuation:
            out += sep
        out += word
    return out

def parse_words(m):
    return list(map(parse_word, m.dgndictation[0]._words))

def insert(s):
    Str(s)(None)

def slap_with(s):
    return([Key('ctrl-e'),"%s\n"%s])

def op_equal(s):
    return(" %s= "%s)

def text(m):
    insert(join_words(parse_words(m)).lower())

def sentence_text(m):
    text = join_words(parse_words(m)).lower()
    insert(text.capitalize())

def word(m):
    text = join_words(list(map(parse_word, m.dgnwords[0]._words)))
    insert(text.lower())

def surround(by):
    def func(i, word, last):
        if i == 0: word = by + word
        if last: word += by
        return word
    return func

def rot13(i, word, _):
    out = ''
    for c in word.lower():
        if c in string.ascii_lowercase:
            c = chr((((ord(c) - ord('a')) + 13) % 26) + ord('a'))
        out += c
    return out

formatters = {
    'dunder': (True,  lambda i, word, _: '__%s__' % word if i == 0 else word),
    'camel':  (True,  lambda i, word, _: word if i == 0 else word.capitalize()),
    'snake':  (True,  lambda i, word, _: word if i == 0 else '_'+word),
    'dotpath': (True, lambda i, word, _: word if i == 0 else '.'+word),
    'smash':  (True,  lambda i, word, _: word),
    # spinal or kebab?
    'kebab':  (True,  lambda i, word, _: word if i == 0 else '-'+word),
    # 'sentence':  (False, lambda i, word, _: word.capitalize() if i == 0 else word),
    'title':  (False, lambda i, word, _: word.capitalize()),
    'allcaps': (False, lambda i, word, _: word.upper()),
    'dubstring': (False, surround('"')),
    'string': (False, surround("'")),
    'padded': (False, surround(" ")),
    'rot-thirteen':  (False, rot13),
}

def FormatText(m):
    fmt = []
    for w in m._words:
        if isinstance(w, Word):
            fmt.append(w.word)
    try:
        words = parse_words(m)
    except AttributeError:
        with clip.capture() as s:
            press('cmd-c')
        words = s.get().split(' ')
        if not words:
            return

    tmp = []
    spaces = True
    for i, word in enumerate(words):
        word = parse_word(word)
        for name in reversed(fmt):
            smash, func = formatters[name]
            word = func(i, word, i == len(words)-1)
            spaces = spaces and not smash
        tmp.append(word)
    words = tmp

    sep = ' '
    if not spaces:
        sep = ''
    Str(sep.join(words))(None)

def copy_bundle(m):
    bundle = ui.active_app().bundle
    clip.set(bundle)
    app.notify('Copied app bundle', body='{}'.format(bundle))

ctx = Context('input')
ctx.keymap({
    'say <dgndictation> [over]': text,

    '(senten|sentence) <dgndictation> [over]': sentence_text,
    '(cam|comma) <dgndictation> [over]': [', ', text],
    '(period|stop) <dgndictation> [over]': ['. ', sentence_text],
    'more <dgndictation> [over]': [' ', text],
    'word <dgnwords>': word,

    '(%s)+ [<dgndictation>]' % (' | '.join(formatters)): FormatText,

    # more keys and modifier keys are defined in basic_keys.py

    'slap': slap_with(''),
    'question [mark]': '?',
    'tilde': '~',
    '(bang | exclamation point | exclaim | clam)': '!',
    '(dollar [sign])': '$',
    '(ska | downscore)': '_',
    '(coal | colon)': ':',

    '(splat | star | asterisk | asterix)': '*',
    '(hash [sign] | number sign)': '#',
    'percent [sign]': '%',
    'caret': '^',
    'at sign | lat': '@',
    '(and sign | ampersand | amper)': '&',
    'pipe': '|',

    'triple quote': "'''",

    '(dot dot | dotdot)': '..',
    '(dot dot dot | dot-dot-dot)': '...',
    'quest': '?',
    'greater than': ' > ',
    '(triple arrow | tri-lang)': ' <<< ',
    '(kamslap | kaslap)': slap_with(","),
    'semmap': slap_with(';'),
    '(coalpaa | colpaa)': ': ',

    '(arrow | stabby)': '->',

    'plus': '+',
    'indirect': '&',
    'dereference': '*',
    '(op equals | spequal[s] | assign)': ' = ',
    'op (minus | subtract)': ' - ',
    'op (plus | add)': ' + ',
    'op (times | multiply)': ' * ',
    'op divide': ' / ',
    'op mod': ' % ',
    '[op] (minus | subtract) equal[s]': ' -= ',
    '[op] (plus | add) equal[s]': ' += ',
    '[op] (times | multiply) equal[s]': ' *= ',
    '[op] divide equal[s]': ' /= ',
    '[op] mod equal[s]': ' %= ',

    '(op | is) greater [than]': ' > ',
    '(op | is) less [than]': ' < ',
    '(op | is) equal': ' == ',
    '[(op | is)] (streak | E Q)': ' eq ',
    '(op | is) not equal': ' != ',
    '(op | is) greater [than] or equal': ' >= ',
    '(op | is) less [than] or equal': ' <= ',
    '(op (power | exponent) | to the power [of])': ' ** ',
    'op and': ' && ',
    'op or': ' || ',
    '[op] (logical | bitwise) and': ' & ',
    '[op] (logical | bitwise) or': ' | ',
    '(op | logical | bitwise) (ex | exclusive) or': ' ^ ',
    '[(op | logical | bitwise)] (left shift | shift left)': ' << ',
    '[(op | logical | bitwise)] (right shift | shift right)': ' >> ',
    '(op | logical | bitwise) and equals': ' &= ',
    '(op | logical | bitwise) or equals': ' |= ',
    '(op | logical | bitwise) (ex | exclusive) or equals': ' ^= ',
    '[(op | logical | bitwise)] (left shift | shift left) equals': ' <<= ',
    '[(op | logical | bitwise)] (right shift | shift right) equals': ' >>= ',

    'plus-plus': '++',
    'minus-minus': '--',

    'spive': ' -',
    'pive': '- ',
    'pivak': '- [ ]',
    'scoll': ': ',
    'spipe': ' | ',
    'splus': ' + ',
    'spore-equal': ' ||= ',
    'spur-equal': ' //= ',
    "or-equal": "||=",
    "err-equal": "//=",
    "cama": ", ",
    "cola": ": ",
    "equal-cola": "=: ",
    "dolaip": ['$()', Key('left')],
    "dolace": ['${}', Key("left")],
    "(slace|splace)": " {",
    "streek[-you]": " eq ",
    "strneek": " ne ",
    "strcump": " cmp ",
    "spry": " )",
    "(srace|sprace)": " }",
    "(UFO|you-foe|spaceship)": " <=> ",
    'lote': '("',

    'shebang bash': '#!/bin/bash -u\n',

    'new window': Key('cmd-n'),
    'next window': Key('cmd-`'),
    'last window': Key('cmd-shift-`'),
    'next app': Key('cmd-tab'),
    'last app': Key('cmd-shift-tab'),
    'next tab': Key('ctrl-tab'),
    'new tab': Key('cmd-t'),
    'last tab': Key('ctrl-shift-tab'),

    'next space': Key('cmd-alt-ctrl-right'),
    'last space': Key('cmd-alt-ctrl-left'),

    'scroll down': [Key('down')] * 30,
    'scroll up': [Key('up')] * 30,

    'copy active bundle': copy_bundle,
})

