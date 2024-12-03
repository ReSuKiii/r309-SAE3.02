'''Le projet présenté dans le document est une SAÉ (Situation d'Apprentissage et d'Évaluation). Il s'agit de concevoir et développer un système informatique distribué avec plusieurs serveurs, permettant de gérer des clients qui envoient des programmes à exécuter. Voici une explication simple du concept et des étapes pour y parvenir :
Concept de la SAE

Le projet vise à créer une architecture client-serveur distribuée, où :

    Les clients :
        Envoient des programmes à un serveur via une interface graphique.
        Reçoivent les résultats de l'exécution ou les erreurs.

    Les serveurs :
        Un serveur principal (maître) reçoit les demandes des clients.
        Si le serveur maître est surchargé, il délègue des tâches à des serveurs secondaires (esclaves).
        Les serveurs secondaires exécutent les programmes et retournent les résultats au maître.

    Objectifs :
        Gérer efficacement plusieurs clients simultanément.
        Répartir la charge entre les serveurs pour éviter les surcharges.
        Maintenir un système robuste, scalable et sécurisé.

Étapes pour réaliser la SAE
1. Analyse du Projet

    Comprendre les besoins :
        Communication client-serveur.
        Gestion de plusieurs clients.
        Répartition de charge (load balancing).
    Identifier les contraintes techniques :
        Utilisation de sockets pour la communication.
        Surveillance de la charge CPU/mémoire.

2. Planification et Architecture

    Définir une architecture distribuée :
        Un serveur maître pour coordonner les tâches.
        Plusieurs serveurs secondaires pour exécuter les tâches.
        Un client avec interface graphique.
    Planifier les modules principaux :
        Communication réseau (sockets).
        Gestion des tâches (exécution de programmes).
        Load balancing (distribution des tâches).
    Prévoir des extensions possibles (sécurité, monitoring, etc.).

3. Développement

    Création du Client :
        Interface graphique pour saisir l'adresse IP, le port, et le programme à exécuter.
        Envoi du programme au serveur maître.
        Réception des résultats d'exécution.

    Développement du Serveur Maître :
        Gestion des connexions avec plusieurs clients.
        Surveillance de sa propre charge (nombre de programmes, utilisation CPU).
        Envoi des tâches à des serveurs secondaires en cas de surcharge.

    Développement des Serveurs Secondaires :
        Réception des tâches du serveur maître.
        Exécution des programmes (par exemple, avec un interpréteur Python ou GCC).
        Envoi des résultats au serveur maître.

    Communication :
        Utiliser des sockets pour échanger les données (TCP recommandé pour fiabilité).
        Gérer les erreurs (perte de connexion, etc.).

4. Tests et Débogage

    Tester la communication entre client et serveur.
    Simuler plusieurs clients pour vérifier la gestion de la charge.
    Vérifier que les serveurs secondaires reçoivent et exécutent correctement les tâches.

5. Optimisation et Fonctionnalités Avancées

    Ajouter des fonctionnalités supplémentaires :
        Monitoring en temps réel du cluster (état des serveurs, charge, etc.).
        Persistante des données pour relancer les tâches en cas d’échec.
        Sécurisation des échanges avec des protocoles comme SSL/TLS.
    Améliorer la scalabilité pour permettre d’ajouter dynamiquement de nouveaux serveurs.
    '''