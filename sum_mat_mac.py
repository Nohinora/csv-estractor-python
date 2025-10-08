import csv
import common_data

with open('power_coffee.csv','r') as f:
    dicReader = csv.DictReader(f)

    sum_mat = 0
    sum_mac = 0

    for line in dicReader:
        for i in range(24):
            matricola = line['matricola ' + str(i+1)]
            if matricola != '':
                sum_mat += 1
                # print(matricola)
        for model in common_data.models.keys():
            if line[model] != '':
                sum_mac += int(line[model])
    
    print(f'macchine = {sum_mac}')
    print(f'matricole = {sum_mat}')
