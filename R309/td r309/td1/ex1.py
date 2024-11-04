'''
Questions :
# 1. Que fait ce code ?

Ce code permet de diviser un entier x par un entier y en utilisant la soustraction.

# 2. Essayer avec deux valeurs simples (entiers et positifs) ?

divEntier(10, 2) = 5
divEntier(10, 3) = 3

# Exercices :

# 1. Ajouter un main permettant de saisir les valeurs de x et de y.

# 2. Ajouter l’exception ValueError

    a. Pourquoi devez-vous gérer ValueError ?

Car l'utilisateur peut saisir autre chose qu'un entier et cela génère une erreur


# 3. Essayer de saisir la valeur 0 pour y

    a. Que se passe-t-il ?

On a une erreur de type recursionError car la fonction divEntier est appelée de manière infinie

    b. Gérer l’exception en mettant un message correspondant à l’erreur    

# 4. Ajouter dans la fonction divEntier une exception :

    a. si l’un des nombres passés par argument est négatif
    b. si y est égale à 0

'''

def divEntier(x: int, y: int) -> int:
    if y == 0: # ex 4
        raise ValueError("Division par 0 impossible")
    if x < 0 or y < 0: # ex 4
        raise ValueError("Division par un nombre négatif impossible")
    if x < y:
        return 0
    else:
        x = x - y
    return divEntier(x, y) + 1

def main(): # ex 1
    try:
        x = int(input("Saisir x: ")) # ex 1
        y = int(input("Saisir y: ")) # ex 1
        print(divEntier(x, y))
    except ValueError: # ex 2 -> pas 100% nécessaire car on a déjà une exception ValueError dans divEntier 
        print("Veuillez saisir un entier")
    except Exception as e: # ex 3
        print(e)


if __name__ == "__main__":
    main()
