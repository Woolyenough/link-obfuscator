import random

MODES = {
    'default': 'Default Mode',
    'xd': 'XD Mode',
    'lol': 'LOL Mode',
}

def generate_code(mode):
    if mode == 'xd':
        chars = ['xd', 'XD', 'xD', '!']
        return ''.join(random.choice(chars) for _ in range(5,10))
    elif mode == 'lol':
        options = ['lol', 'LOL', 'lmao', 'LMAO','!']
        return ''.join(random.choice(options) for _ in range(5,10))
    else:
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
