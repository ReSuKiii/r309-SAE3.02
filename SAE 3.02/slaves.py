import socket
import subprocess
import os
import time
import threading
import sys

class ServeurEsclave:
    def __init__(self, hote='localhost', port=0):
        self.hote = hote
        self.port = port
        self.en_cours = True 

    def demarrer(self):
        try:
            self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_serveur.bind((self.hote, self.port))
            self.socket_serveur.listen(1)
            self.port = self.socket_serveur.getsockname()[1]
            print(f"Esclave en écoute sur {self.hote}:{self.port}")
            time.sleep(1)
        except OSError as e:
            print(f"Erreur lors de la liaison du socket: {e}")
            return

        while self.en_cours:
            try:
                socket_client, _ = self.socket_serveur.accept()
                threading.Thread(target=self.gerer_client, args=(socket_client,), daemon=True).start()
            except Exception as e:
                print(f"Erreur lors de l'acceptation du client: {e}")

    def executer_programme(self, chemin_fichier):
        try:
            if chemin_fichier.endswith('.py'):
                resultat = subprocess.run(['python3', chemin_fichier], capture_output=True, text=True)
            elif chemin_fichier.endswith('.java'):
                resultat_compilation = subprocess.run(['javac', chemin_fichier], capture_output=True, text=True)
                if resultat_compilation.returncode != 0:
                    return f"Erreur de compilation: {resultat_compilation.stderr}"
                nom_classe = os.path.splitext(os.path.basename(chemin_fichier))[0]
                resultat = subprocess.run(['java', nom_classe], capture_output=True, text=True)
            elif chemin_fichier.endswith('.c'):
                executable = os.path.splitext(chemin_fichier)[0]
                resultat_compilation = subprocess.run(['gcc', chemin_fichier, '-o', executable], capture_output=True, text=True)
                if resultat_compilation.returncode != 0:
                    return f"Erreur de compilation: {resultat_compilation.stderr}"
                resultat = subprocess.run([executable], capture_output=True, text=True)
            else:
                return "Type de fichier non pris en charge."

            if resultat.returncode == 0:
                return resultat.stdout
            else:
                return f"Erreur d'exécution: {resultat.stderr}"

        except Exception as e:
            return f"Erreur d'exécution: {e}"

    def gerer_client(self, socket_client):
        try:
            while True:
                en_tete = socket_client.recv(4096).decode()
                if not en_tete:
                    break  
                if en_tete.startswith("STOP"):
                    print("Commande d'arrêt reçue. Arrêt de l'esclave.")
                    socket_client.sendall("Esclave en cours d'arrêt.".encode())
                    self.en_cours = False
                    return
                elif en_tete.startswith("FILE"):
                    try:
                        _, nom_fichier, taille_fichier = en_tete.split('|')
                        taille_fichier = int(taille_fichier)
                    except ValueError as e:
                        print(f"Erreur lors de l'analyse de l'en-tête: {e}")
                        socket_client.sendall(f"Erreur lors de l'analyse de l'en-tête: {e}".encode())
                        continue

                    chemin_fichier = os.path.join(os.getcwd(), nom_fichier)

                    with open(chemin_fichier, 'wb') as f:
                        total_recu = 0
                        while total_recu < taille_fichier:
                            morceau = socket_client.recv(min(4096, taille_fichier - total_recu))
                            if not morceau:
                                break
                            f.write(morceau)
                            total_recu += len(morceau)

                    print(f"Fichier {nom_fichier} reçu. Exécution en cours...")
                    resultat = self.executer_programme(chemin_fichier)
                    socket_client.sendall(resultat.encode())
                elif en_tete.startswith("TEXT"):
                    texte = en_tete[5:]
                    print(f"Texte reçu: {texte}")
                    reponse = f"Texte reçu: {texte}"
                    socket_client.sendall(reponse.encode())
                else:
                    socket_client.sendall("Commande inconnue.".encode())
        except Exception as e:
            print(f"Erreur lors de la gestion du client: {e}")
        finally:
            time.sleep(1)
            socket_client.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 0
    serveur_esclave = ServeurEsclave(port=port)
    serveur_esclave.demarrer()
