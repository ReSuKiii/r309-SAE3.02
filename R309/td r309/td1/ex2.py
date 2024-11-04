'''
Question de fichiers
Voici les différentes étapes à réaliser :
1. Ouvrir un fichier texte (existant) en lecture dont le nom est spécifié dans une variable
2. Afficher les lignes du fichier
   a. Vous pourriez avoir à utiliser la fonction rstrip pour enlever les \n et les \r
3. Fermer le fichier


Gérer les exceptions des fichiers :
Voici les différentes exceptions, donnez un message en français expliquant l’erreur pour
chacune des exceptions :
• FileNotFoundError
• IOError
• FileExistsError
• PermissionError
Ajouter un finally pour expliquer que c’est la fin du programme.
Essayer avec des fichiers existants ou non


Ouverture d’un fichier avec with
Je ne vais pas m’étendre sur le management de contexte de python ici mais vous pouvez lire
des informations en recherchant sur le web. Ils sont utilisés pour gérer les ressources et
notamment les fichiers en s’assurant que les ressources utilisées sont libérées lorsque le
contexte est terminé (par exemple que le fichier soit clos).
Voici un exemple :


with open('fichier.txt', 'r') as f:
    for l in f:
        l = l.rstrip("\n\r")
        print(l)

Néanmoins, les exceptions doivent être gérées. Ajouter les exceptions nécessaires dans ce code
'''

fichier = input("Saisir le nom du fichier: ")



try:
    with open(fichier, 'r') as f:
        for l in f:
            l = l.rstrip("\n\r")
            print(l)
        f.close()
except FileNotFoundError:
    print("Fichier non trouvé")
except IOError:
    print("Erreur d'entrée/sortie")
except FileExistsError:
    print("Fichier déjà existant")
except PermissionError:
    print("Permission refusée")
finally:
    print("Fin du programme")
