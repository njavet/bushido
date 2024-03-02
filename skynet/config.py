# database name
db_name = 'skynet.db'


# profile
default_pic = 'images/profile_pics/default.png'


# emojis
emojis = {
    b'\xe2\x9a\x96\xef\xb8\x8f'.decode(): 'balance',

    b'\xf0\x9f\xaa\x90'.decode(): 'wimhof',

    b'\xf0\x9f\xa6\x8d'.decode(): 'gym.resistance',
    b'\xf0\x9f\xa5\x8b'.decode(): 'gym.martial_arts',

    b'\xe2\x9b\xa9\xef\xb8\x8f'.decode(): 'resistance.squat',
    b'\xf0\x9f\x8f\x97\xef\xb8\x8f'.decode(): 'resistance.deadlift',
    b'\xf0\x9f\x9a\x81'.decode(): 'resistance.benchpress',
    b'\xf0\x9f\xa6\xad'.decode(): 'resistance.overheadpress',
    b'\xf0\x9f\x90\xa2'.decode(): 'resistance.rows',

    b'\xf0\x9f\xa6\x85'.decode(): 'resistance.pullups',
    b'\xf0\x9f\x8c\x90'.decode(): 'resistance.pushups',

    b'\xf0\x9f\xaa\x96'.decode(): 'cardio.running',

    b'\xe2\x9a\x94\xef\xb8\x8f'.decode(): 'chrono.splitmachine',
    b'\xf0\x9f\x8f\xb9'.decode(): 'chrono.stretch',
    b'\xf0\x9f\x94\xa5'.decode(): 'chrono.naulikriya',
}

# emojis
single2double = {
    b'\xe2\x9b\xa9': b'\xe2\x9b\xa9\xef\xb8\x8f',  # shinto -> squats
    b'\xf0\x9f\x8f\x97': b'\xf0\x9f\x8f\x97\xef\xb8\x8f',  # crane -> deadlift'
    b'\xe2\x9a\x94': b'\xe2\x9a\x94\xef\xb8\x8f',  # sword -> split_machine
    b'\xe2\x9a\x96': b'\xe2\x9a\x96\xef\xb8\x8f',  # balance
}

