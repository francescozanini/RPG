def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def display_option(sentence, options):
    i = 1
    print(sentence)
    for item in options:
        print(str(i) + ':', item)
        i += 1
    choice = input('Choose action:')
    return choice

def get_user_input(options, mssg='\nWhat do you want to do?'):
    sensible_input = False
    while not (sensible_input):
        user_input = display_option(mssg, options)
        if is_integer(user_input):
            user_input = int(user_input)
            sensible_input = user_input > 0 and user_input <= len(options)
        if not(sensible_input):
            print("\nAction not recognized!")
    return user_input