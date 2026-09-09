f, i, o = input('ФИО: ').split()
b = f"{f[0].upper()}{i[0].upper()}{o[0].upper()}."
print(f'Инициалы: {b}')
print(f'Длина (символов): {len(f + ' ' + i + ' ' + o)}')