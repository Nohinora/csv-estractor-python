import csv
import common_data
import re
import sys

fieldnames = ["date", "ddt", "model", "matricola", "shop", "legacy","verified","no_mat_found","negative_model_number"]

def extract(dic_reader, SHOP, MAT):
    data_to_write = []

    no_mat_count = 0 # matricola da dare alle macchine senza
    num_of_mat = count_mat_columns(dic_reader)

    for line in dic_reader:
        # Estrazione matricole del giorno
        matricole = []
        for i in range(num_of_mat):
            matricola = line['matricola' + str(i+1)]
            if matricola != '':
                matricole.append(matricola)

        # Associazione macchine a matricole del giorno in base alle matricole descritte dalle espressioni
        for model in common_data.models.keys():
            if line[model] == '': continue # se ci sono zero modelli passo a quello successivo
            
            model_amount = int(line[model]) # numero di macchine corrispondenti a questo modello
            negative_model_number = 0

            if model_amount < 0:
                negative_model_number = 1
                model_amount *= -1

            for i in range(model_amount): # inizio il cilclo per l'associazione matricola modello, itero per il numero di modelli
                for idx, matricola in enumerate(matricole): # itero per cercare una corrispondenza nel vettore delle matricole del giorno
                    if re.search(common_data.models[model],matricola): # in caso di corrispondenza elimino la matricola dal vettore, diminuisco la conta del modello corrente e esco da questo ciclo poichè ho associato al modello corrente la sua matricola
                        matricole.pop(idx)
                        model_amount -= 1
                        data_to_write.append(generate_entry(line, model, matricola, SHOP, 0, negative_model_number))
                        break

            # Handle macchine senza matricole
            while model_amount > 0:
                model_amount -= 1
                no_mat_count += 1
                print(f"{line['date']}, {model}, {MAT}-{no_mat_count:03}")
                data_to_write.append(generate_entry(line, model, f"{MAT}-{no_mat_count:03}", SHOP, 1, negative_model_number))
        
        # matricole avanzate
        if len(matricole) > 0:
            for matricola in matricole:
                data_to_write.append(generate_entry(line, matricola_avanzata(matricola), matricola, SHOP, 0, negative_model_number))
    
    return data_to_write

    

# FUNCTIONS

def generate_entry(line, model, matricola, shop, no_mat, negative_model_number):
    entry = {
        "date": line["date"],
        "ddt": line["ddt"],
        "model": model,
        "matricola": matricola,
        "shop": shop,
        "legacy": 1,
        "verified": 0,
        "no_mat_found": no_mat,
        "negative_model_number": negative_model_number
    }
    return entry

def count_mat_columns(dicReader):
    count = 0
    for field in dicReader.fieldnames:
        if re.search("matricola", field):
            count += 1
    return count

def matricola_avanzata(matricola):
    poss_models = "MA"
    for key in common_data.models:
        if re.search(common_data.models[key],matricola):
            poss_models += ("_" + key)
    return poss_models



if __name__ == "__main__":
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    shop_name = str(sys.argv[3])
    no_mat_prefix = str(sys.argv[4])

    dic_reader = csv.DictReader(open(input_file, "r"))

    data_to_write = extract(dic_reader, shop_name, no_mat_prefix)

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_to_write)