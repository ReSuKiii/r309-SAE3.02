# Documentation d'installation et d'utilisation

## Prérequis

- Python 3.x
- PyQt5 (pour le client)
- GCC (pour compiler les fichiers C)
- JDK (pour compiler et exécuter les fichiers Java)


## Installation

### Serveur

1. Clonez le dépôt ou téléchargez les fichiers du serveur.
2. Assurez-vous que Python 3.x est installé sur votre machine.
3. Installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

### Client

1. Clonez le dépôt ou téléchargez les fichiers du client.
2. Assurez-vous que Python 3.x est installé sur votre machine.
3. Installez PyQt5 :
    ```bash
    pip install PyQt5
    ```

## Utilisation

### Démarrage du serveur

1. Naviguez vers le répertoire contenant les fichiers du serveur et ouvrez le fichier `server_test.py`.
2. Modifier la ligne 209 et remplacez `/DossierMaitre-Slave/` par le dossier contenant vos serveurs
3. Exécutez le script `server_test.py` :
4. Le serveur démarrera et écoutera les connexions sur le port 4200 par défaut.

### Démarrage du client

1. Naviguez vers le répertoire contenant les fichiers du client.
2. Exécutez le script `client_test.py` :
3. Une interface graphique s'ouvrira. Entrez l'hôte (par défaut `localhost`) et le port (par défaut `4200`), puis cliquez sur "Se connecter".

### Envoi de messages

1. Une fois connecté, entrez un message dans le champ "Message à envoyer".
2. Cliquez sur "Envoyer" pour envoyer le message au serveur.

### Envoi de fichiers

1. Cliquez sur "Choisir un fichier" pour sélectionner un fichier à envoyer.
2. Cliquez sur "Envoyer le fichier" pour envoyer le fichier au serveur.

### Arrêt du serveur

1. Cliquez sur "Arrêter le serveur" pour envoyer une commande d'arrêt au serveur.
2. Le serveur et tous les esclaves connectés s'arrêteront.

## Structure des fichiers

- `server_test.py` : Script principal du serveur.
- `client_test.py` : Script principal du client.
- `slaves_test.py` : Script pour les serveurs esclaves (doit être dans le même dossier que le serveur maitre).
- `requirements.txt` : Liste des dépendances nécessaires pour le serveur.

## Remarques

- Assurez-vous que les ports utilisés ne sont pas bloqués par un pare-feu.
- Pour tester avec plusieurs clients, exécutez plusieurs instances du script `client_test.py`.
- Pour tester avec plusieurs serveurs esclaves, envoyez plusieurs fichiers ou messages pour observer la gestion des charges.


## Problèmes connu :

 - apres nimporte quelle action, le client se ferme. Ca n'arrive pas souvent et je pense avoir regler le problème mais on ne sait jamais.
 - envois trop rapide : si on envois 2 fichiers en appuyant rapidementr sur envoi avec le client, aucun de ces fichiers ne sera traité correctement, le serveur esclave n'as pas le temps d'executer.
 - acces non autorisé (C) : Pendant le traitement du code C il m'est arrivé d'avoir l'erreur `Acces non autorisé`, je ne sais pas exactement pourquoi mais le fix était de supprimer le fichier C et réessayer.