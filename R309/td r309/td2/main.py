'''Exercice 1 : Créer deux threads qui impriment chacun un message différent 5 fois avec un
petit délai entre chaque affichage
Je suis la thread 1
Je suis la thread 2
Je suis la thread 1
Je suis la thread 1
Je suis la thread 2
Je suis la thread 1
Je suis la thread 2
Je suis la thread 2
Je suis la thread 1
Exercice 2 : Créer deux threads de compte à rebours avec des valeurs de départ différentes.
thread 1 : 5
thread 1 : 4
thread 2 : 3
thread 1 : 3
thread 2 : 2
thread 2 : 1
thread 1 : 2
thread 1 : 1
Exercice 3 : Reprenez l’exercice du cours sur le pool de thread
Exercice 4 : si vous avez le temps / l’envie : refaire les exercices 1 et 2 avec des processus et
comparer les temps d’exécution.'''

# ex 1
import threading
import time



def ex1():
    def thread1():
        for i in range(5):
            print("Je suis la thread 1")
            time.sleep(0.5)

    def thread2():
        for i in range(5):
            print("Je suis la thread 2")
            time.sleep(0.5)

    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
  
def ex2():
    def countdown(n):
        while n>0:
            print(f"thread 1 : {n}")
            time.sleep(0.5)
            n -= 1
    def countdown2(n):
        while n>0:
            print(f"thread 2 : {n}")
            time.sleep(0.5)
            n -= 1
    t1 = threading.Thread(target=countdown, args=(5,))
    t2 = threading.Thread(target=countdown2, args=(3,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    # ex1()
    ex2()
    

