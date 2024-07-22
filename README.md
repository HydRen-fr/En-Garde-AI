![Image du jeu](/doc/engarde.png)

Ce répertoire propose différents programmes informatiques autour du jeu En Garde conçu par Reiner Knizia. Je joue à ce jeu depuis que je suis petit, et étant un amateur et un étudiant d'informatique, j'ai eu l'idée de concevoir une IA imbattable à ce jeu. Le programme nommé "Humain_Ordinateur" permet à un humain d'affronter un ordinateur qui joue des coups au hasard. Le programme nommé "Ordinateur_Ordinateur" permet de faire une simulation d'une partie aléatoire à En Garde. Le programme nommé "Humain_IA" permet à un humain d'affronter une IA dont la stratégie se base sur un nombre important de simulations à chaque tour afin de déterminer le meilleur coup grâce à un simple ratio victoires/défaites.

Remarques :
- Les règles du jeu En Garde sont disponibles en pdf.
- Le principe de la première IA est très élémentaire. Une IA qui fonctionnerait grâce à Minimax ou MCTS serait bien évidemment plus performante.
- La défense de l'IA est au hasard en elle-même, mais la possibilité de devoir se défendre est prise en compte dans les simulations.
- Coder l'IA en C++ au lieu de Python permettrait de faire 26 fois plus de simulations par tour, avec le même temps.
- Je respecte entièrement le travail de Reiner Knizia et le remercie pour avoir conçu ce jeu. Je n'ai aucune intention de lui porter préjudice en rendant gratuit d'accès En Garde, et de toute façon, l'absence de graphiques fait que personne ne peut avoir envie d'utiliser plus de deux fois ces programmes, et cela pourrait même pousser à acheter le jeu, que je recommande vivement.
- Un programme bonus nommé "Assistant" permet à une personne, qui joue contre quelqu'un d'autre au jeu de société réel, de se faire assister par l'IA. Il faut rentrer dans le code du programme la main du joueur qui veut se faire assister, ainsi que la défausse, les positions sur le plateau, et enfin si le joueur assisté a l'escrimeur de gauche ou de droite. Les règles stipulent qu'on ne peut pas regarder le contenu de la défausse, mais rien n'empêche de le retenir 🙂.
