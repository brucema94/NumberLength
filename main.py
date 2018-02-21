# dictionary that knows how many syllables are in certain numbers
length_dict = {'1':  1, '2':  1, '3':  1, '4':  1, '5':  1, '6':  1, '7':  2,
               '8':  1, '9':  2, '10':  1, '11': 1, '12': 1, '13': 2, '14': 2,
               '15': 2, '16': 2, '17': 3, '18': 2, '19': 3, '20':  2, '100': 2,
               '1000': 2, '1000000': 2, '1000000000': 2}


def get_length(number: str):
    """
    Calculates the number of syllables in a number
    :param number: String representation of the number
    :return: number of syllables
    """
    # 00100 should ingore leading zeros
    number = number.lstrip('0')
    # an empty number takes no time to pronounce
    if number == '':
        return 0

    # cache an integerized version of number for efficiency
    int_number = int(number)
    # special cases that the dictionary knows
    if number in length_dict:
        return length_dict[number]
    elif int_number < 100:
        # other numbers under 100 are structured as 'twee en tachtig',
        # both of which the dict knows
        return length_dict[number[:1] + '0'] + 1 + length_dict[number[1:]]
    elif int_number < 1000:
        # numbers are pronounced 'negen honderd tweeëntachtig',
        # each of which the function can handle
        # if leading number is one, not pronounced
        leading_n_syllable = get_length(number[:1]) if number[:1] != '1' \
                                  else 0
        return leading_n_syllable + length_dict['100'] + get_length(number[1:])
    elif int_number < 1000000:
        # numbers are pronounced
        # 'honderdachtentwintig duizend negenhonderdtweeëntachtig'
        # if leading number is one, not pronounced
        leading_n_syllable = get_length(number[:1]) if number[:1] != '1' else 0
        return leading_n_syllable + length_dict['1000'] + \
            get_length(number[-3:])
    elif int_number < 1000000000:
        # handling of numbers of the form
        # 'driehonderachtien miljoen hnderachtentwintigduizendnegenhonderdtweeëntachtig'
        return get_length(number[:-3]) + length_dict['1000000'] + \
            get_length(number[-6:])
    elif int_number < 1000000000000:
        # etc
        return get_length(number[:-3]) + length_dict['1000000000'] + \
            get_length(number[-9:])


# compute the time in years required to pronounce all numbers up to 1 billion
# assuming 5 syllables per second
sum = 0
for i in range(1000000000):
    sum += get_length(str(i))
print(sum / 5.0 / 3600.0 / 24.0 / 365.0)
