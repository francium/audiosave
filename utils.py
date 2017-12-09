def yesno(msg: str) -> bool:
    choice = ''
    while choice.lower() not in ['y', 'n', 'yes', 'no']:
        choice = input(msg.strip() + ' ')

    return True if choice[0].lower() == 'y' else False
