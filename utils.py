def yesno(message):
    choice = None
    while choice != 'y' and choice !='n':
        choice = input(message + ' ')

    return True if choice == 'y' else False
