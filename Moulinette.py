import csv
import os
import sys
from datetime import date, time, datetime
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from pyparsing import empty


file_name_caracteristiques = "/home/renando/PycharmProjects/BigData/original_csv/caracteristiques_2009.csv"
out_file_name_caracteristiques = "/home/renando/PycharmProjects/BigData/new_csv/NEW_caracteristiques_2009.csv"

file_name_lieu = "/home/renando/PycharmProjects/BigData/original_csv/lieux_2009.csv"
out_file_name_lieu = "/home/renando/PycharmProjects/BigData/new_csv/NEW_lieux_2009.csv"

file_name_usagers = "/home/renando/PycharmProjects/BigData/original_csv/usagers_2009.csv"
out_file_name_usagers = "/home/renando/PycharmProjects/BigData/new_csv/NEW_usagers_2009.csv"

file_name_vehicules = "/home/renando/PycharmProjects/BigData/original_csv/vehicules_2009.csv"
out_file_name_vehicules = "/home/renando/PycharmProjects/BigData/new_csv/NEW_vehicules_2009.csv"

special_caractere = ['-', ' ', ',', ';', '|', '', '#', '*', '.', '!', '?']


def check_file_exists(chemin_fichier):
    if not os.path.isfile(chemin_fichier):
        sys.exit("Le fichier "+os.path.splitext(chemin_fichier)[0]+" n'a pas été trouvé")


def convert_year_month_day_hour_min_to_date(mois, jour, heure_minute):
    """
    Permet de convertir en date
    :param mois:
    :param jour:
    :param heure_minute:
    :return:
    """
    if mois.strip() is not "" and jour.strip() is not "":
        d = date(2009, int(mois), int(jour))
    else:
        return ""
    if heure_minute.strip() is not empty and len(heure_minute) > 2:
        t = time(int(heure_minute[:-2]), int(heure_minute[-2:]))
        date_complet = datetime.combine(d, t)
    elif len(heure_minute) == 2:
        t = time(00, int(heure_minute[-2:]))
        date_complet = datetime.combine(d, t)
    else:
        return d
    return date_complet


def case_not_null(valeur):
    """
    Permet d'avoir des cases vide au lieu de null ou caractere spéciaux
    :param valeur:
    :return:
    """
    if valeur in special_caractere:
        return ""
    else:
        if type(valeur) is int:
            return int(valeur)
        elif type(valeur) is str:
            return str(valeur)
    return valeur


def case_not_null_commune(valeur):
    """
    Permet d'avoir des cases vide au lieu de null ou caractere spéciaux
    :param valeur:
    :return:
    """
    if valeur in special_caractere:
        return ""
    else:
        valeur = str(valeur)
        while len(valeur) < 3:
            valeur += "0"
        return int(valeur)


def case_not_null_between(valeur, min_val, max_val):
    """
    Valeur doit etre un int contenu entre min et max
    :param valeur:
    :param min_val:
    :param max_val:
    :return:
    """
    if valeur in special_caractere and min_val == 0:
        return "0"
    elif valeur in special_caractere:
        return ""
    else:
        if type(valeur) is int and (min_val <= valeur <= max_val):
            return int(valeur)
    return valeur


def case_not_null_between_catv(valeur):
    """
    Valeur doit etre un int contenu entre min et max
    :param valeur:
    :return:
    """
    if valeur in special_caractere:
        return "0"
    else:
        valeur = int(valeur)
        if 1 <= valeur <= 40 or valeur == 99:
            return int(valeur)
    return ""


def case_not_null_secu(valeur):
    """
    Valeur doit etre un int contenu entre min et max
    :param valeur:
    :return:
    """
    if valeur in special_caractere:
        return "0"
    if valeur is not "":
        valeur = int(valeur)
        if 1 <= valeur <= 3 or valeur == 9 or 11 <= valeur <= 13 or 21 <= valeur <= 23 \
                or 31 <= valeur <= 33 or 41 <= valeur <= 43 or 91 <= valeur <= 93:
            return int(valeur)
    return ""


def case_not_null_between_letter(valeur, letters):
    """
    Valeur doit etre un string contenu dans letters
    :param valeur:
    :param letters:
    :return:
    """
    if valeur in special_caractere:
        return ""
    else:
        if type(valeur) is str and valeur in letters:
            return str(valeur)
    return ""


def special_adresse(adresse):
    """
    On retire les caracteres spéciaux au debut d'un string et on change les abreviation de route, rond, boulevard
    :param adresse:
    :return:
    """
    if adresse.strip() is not "":
        i = 0
        while adresse[i] in special_caractere:
            i += 1
        adresse = str(adresse[i:]).upper()
        if adresse.partition(' ')[0] == "RTE":
            adresse = adresse.replace("RTE","ROUTE",1)
        adresse = adresse.replace(" RTE "," ROUTE ")
        adresse = adresse.replace("RD POINT","ROND POINT")
        adresse = adresse.replace(" BD ","BOULEVARD ")
    return adresse


def special_code_postal(code_postal):
    """
    On retire le dernier 0 des departements
    :param code_postal:
    :return:
    """
    code_postal = str(code_postal)
    if len(code_postal) > 2 and code_postal[-1] == "0":
        return int(code_postal[:len(code_postal)-1])
    return code_postal


def get_lat_longitude(adresse, lat, long):
    if adresse.strip() is not "" and (lat not in special_caractere and long not in special_caractere):
        try:
            geolocator = Nominatim()
            location = geolocator.geocode(adresse+" FRANCE", timeout=10)
            if location is not None and location.latitude is not "" and location.longitude is not "":
                return [location.latitude, location.longitude]
        except GeocoderTimedOut as e:
            print("Error: geocode failed" + str(e))
    return [0, 0]


print("[DEBUT] caracteristiques_2009")
check_file_exists(file_name_caracteristiques)
check_file_exists(out_file_name_caracteristiques)
with open(file_name_caracteristiques, newline='') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter='	', quoting=csv.QUOTE_MINIMAL)
    with open(out_file_name_caracteristiques, 'w', newline='') as newCSVfile:
        spamwriter = csv.writer(newCSVfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Num_Acc', 'date', 'lum', 'agg', 'int', 'atm', 'col', 'adr', 'gps', 'dep', 'com'])
        for row in readCSV:
            spamwriter.writerow([
                row['Num_Acc'],
                convert_year_month_day_hour_min_to_date((row['mois']), (row['jour']), row['hrmn']),
                case_not_null_between(row['lum'], 0, 5),
                case_not_null_between(row['agg'], 0, 2),
                case_not_null_between(row['int'], 0, 9),
                case_not_null_between(row['atm'], 0, 9),
                case_not_null_between(row['col'], 0, 7),
                special_adresse(case_not_null(row['adr'])),
                case_not_null_between_letter(row['gps'], ['M', 'A', 'G', 'R']),
                special_code_postal(case_not_null(row['dep'])),
                case_not_null_commune(row['com']),
            ])
print('[FIN] fichier caracteristiques_2009')


print("[DEBUT] usagers_2009.csv")
check_file_exists(file_name_usagers)
check_file_exists(out_file_name_usagers)
with open(file_name_usagers, newline='') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    with open(out_file_name_usagers, 'w', newline='') as newCSVfile:
        spamwriter = csv.writer(newCSVfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Num_Acc', 'place', 'catu', 'grav',	'sexe',	'trajet', 'secu', 'locp', 'actp', 'etatp',
                             'an_nais', 'num_veh'])
        for row in readCSV:
            spamwriter.writerow([
                row['Num_Acc'],
                case_not_null_between(row['place'], 1, 9),
                case_not_null_between(row['catu'], 0, 4),
                case_not_null_between(row['grav'], 0, 4),
                case_not_null_between(row['sexe'], 0, 2),
                case_not_null_between(row['trajet'], 0, 9),
                case_not_null_secu(row['secu']),
                case_not_null_between(row['locp'], 0, 8),
                case_not_null_between(row['actp'], 0, 9),
                case_not_null_between(row['etatp'], 0, 3),
                case_not_null_between(row['an_nais'], 1900, 2009),
                case_not_null(row['num_veh']),
            ])
print('[FIN] fichier usagers_2009.csv')


print("[DEBUT] lieux_2009.csv")
check_file_exists(file_name_lieu)
check_file_exists(out_file_name_lieu)
with open(file_name_lieu, newline='') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    with open(out_file_name_lieu, 'w', newline='') as newCSVfile:
        spamwriter = csv.writer(newCSVfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Num_Acc', 'catr', 'voie', 'v1', 'v2', 'circ', 'nbv', 'pr', 'pr1', 'vosp',
                             'prof', 'plan', 'lartpc', 'larrout', 'surf', 'infra', 'situ', 'env1'])
        for row in readCSV:
            spamwriter.writerow([
                row['Num_Acc'],
                case_not_null_between(row['catr'], 0, 9),
                row['voie'],
                row['v1'],
                row['v2'],
                case_not_null_between(row['circ'], 0, 4),
                row['nbv'],
                row['pr'],
                row['pr1'],
                case_not_null_between(row['vosp'], 0, 3),
                case_not_null_between(row['prof'], 0, 4),
                case_not_null_between(row['plan'], 0, 4),
                row['lartpc'],
                row['larrout'],
                case_not_null_between(row['surf'], 0, 9),
                case_not_null_between(row['infra'], 0, 7),
                case_not_null_between(row['situ'], 0, 5),
                row['env1'],

            ])
print('[FIN] fichier lieux_2009.csv')


print("[DEBUT] vehicules_2009.csv")
check_file_exists(file_name_vehicules)
check_file_exists(out_file_name_vehicules)
with open(file_name_vehicules, newline='') as csvfile:
    readCSV = csv.DictReader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    with open(out_file_name_vehicules, 'w', newline='') as newCSVfile:
        spamwriter = csv.writer(newCSVfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Num_Acc', 'catv', 'obs', 'obsm', 'choc', 'manv', 'num_veh'])
        for row in readCSV:
            spamwriter.writerow([
                row['Num_Acc'],
                case_not_null_between_catv(row['catv']),
                case_not_null_between(row['obs'], 0, 16),
                case_not_null_between(row['obsm'], 0, 9),
                case_not_null_between(row['choc'], 0, 9),
                case_not_null_between(row['manv'], 0, 24),
                row['num_veh']
            ])
print('[FIN] fichier vehicules_2009.csv')
