import csv

INFO_MAT_MAC_MISMATCH = True
INFO_DIFF_MAC = False

with open('power_coffee.csv','r') as f:
    reader = csv.reader(f)

    next(reader)

    for line in reader:
        sum_machines = 0
        diff_machines = 0
        sum_matricole = 0
        for i in range(16):
            if line[i+2] != '':
                sum_machines += int(line[i+2])
                diff_machines += 1
        for i in range(24):
            if line[18+i] != '':
                sum_matricole += 1

        if INFO_MAT_MAC_MISMATCH & (sum_matricole != sum_machines):
            print(f'{line[0]}: machines are {sum_machines} but matricole are {sum_matricole}')
        if INFO_DIFF_MAC & (diff_machines > 1):
            print(f'{line[0]}: different_machines: {diff_machines}')
        

