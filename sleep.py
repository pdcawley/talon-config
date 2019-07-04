from talon.voice import Context, ContextGroup
from talon.engine import engine
from talon_plugins import speech

sleep_group = ContextGroup('sleepy')
sleepy = Context('sleepy', group=sleep_group)

sleepy.keymap({
    'snore': lambda m: speech.set_enabled(False),
    'unsnore': lambda m: speech.set_enabled(True),

    'dragon mode': [lambda m: speech.set_enabled(False), lambda m: engine.mimic('wake up'.split())],
    'talon mode': [lambda m: speech.set_enabled(True), lambda m: engine.mimic('go to sleep'.split())],
})
sleep_group.load()
