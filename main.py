import csv
import common_data
import re
import sys

def extract(input_file, output_file, SHOP, MAT):
    no_mat = 0 # matricola da dare alle macchine senza
    count = 0

    data_to_write = []

    with open(input_file,'r') as f:
        dicReader = csv.DictReader(f)

        for line in dicReader:
            # Estrazione matricole del giorno
            matricole = []
            for i in range(24):
                matricola = line['matricola ' + str(i+1)]
                if matricola != '':
                    matricole.append(matricola)

            # Associazione macchine a matricole del giorno in base alle matricole descritte dalle espressioni
            for model in common_data.models.keys():
                if line[model] == '': continue # se ci sono zero modelli passo a quello successivo

                model_ammount = int(line[model]) # numero di macchine corrispondenti a questo modello

                # inizio il cilclo per l'associazione matricola modello, itero per il numero di modelli
                for i in range(model_ammount):

                    # itero per cercare una corrispondenza nel vettore delle matricole del giorno
                    for idx, matricola in enumerate(matricole):

                        # in caso di corrispondenza elimino la matricola dal vettore, diminuisco la conta del modello corrente e esco da questo ciclo poichè ho associato al modello corrente la sua matricola
                        if re.search(common_data.models[model],matricola):
                            matricole.pop(idx)
                            model_ammount -= 1
                            count += 1
                            data_to_write.append({
                                "date": line["date"],
                                "ddt": line["ddt"],
                                "model": model,
                                "matricola": matricola,
                                "shop": SHOP,
                                "legacy": 1,
                                "verified": 0,
                                "no_mat_found": 0
                            })
                            break

                # Handle macchine senza matricole
                if model_ammount != 0:
                    for no_mat_model in range(model_ammount):
                        no_mat += 1
                        count += 1
                        print(f"{line['date']}, {model}, {MAT}-{no_mat:03}")
                        data_to_write.append({
                            "date": line["date"],
                            "ddt": line["ddt"],
                            "model": model,
                            "matricola": f"{MAT}-{no_mat:03}",
                            "shop": SHOP,
                            "legacy": 1,
                            "verified": 0,
                            "no_mat_found": 1
                        })

    print(count) # per coffee energy: 372

    with open(output_file, "w", newline="") as f:
        fieldnames = ["date", "ddt", "model", "matricola", "shop", "legacy","verified","no_mat_found"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_to_write)


if __name__ == "__main__":
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    shop_name = str(sys.argv[3])
    no_mat = str(sys.argv[4])
    extract(input_file, output_file, shop_name, no_mat)