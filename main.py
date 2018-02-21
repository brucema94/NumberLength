
length_dict = {'1':  1, '2':  1, '3':  1, '4':  1, '5':  1, '6':  1, '7':  2, '8':  1, '9':  2, '10':  1,
               '11': 1, '12': 1, '13': 2, '14': 2, '15': 2, '16': 2, '17': 3, '18': 2, '19': 3, '20':  1,
               '1000': 2, '1000000': 2, '1000000000': 2}


def get_length(number):
    number = number.lstrip('0')
    if number == '':
        return 0
    int_number = int(number)
    if int_number <= 20:
        return length_dict[number]
    elif number in ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '1000', '1000000']:
        return length_dict[number]
    elif int_number < 100:
        return length_dict[number[:1] + '0'] + length_dict[number[1:]] + 1
    elif int_number < 1000:
        leading_syllable_length = get_length(number[:1]) if number[:1] != '1' else 0
        return leading_syllable_length + get_length('100') + get_length(number[1:])
    elif int_number < 1000000:
        leading_syllable_length = get_length(number[:-3]) if number[:-3] != '1' else 0
        return leading_syllable_length + get_length('1000') + get_length(number[-3:])
    elif int_number < 1000000000:
        leading_syllable_length = get_length(number[:-6]) if number[:-6] != '1' else 0
        return leading_syllable_length + get_length('1000000') + get_length(number[-6:])
    elif int_number < 1000000000000:
        leading_syllable_length = get_length(number[:-9]) if number[:-9] != '1' else 0
        return leading_syllable_length + get_length('1000000000') + get_length(number[-9:])


sum = 0
for i in range(1000000000):
    sum += get_length(str(i))
print(sum / 5.0 / 3600.0 / 24.0 / 365.0)
