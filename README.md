![Image du jeu](/doc/engarde.png)

This directory features various computer programs based on the game En Garde, designed by Reiner Knizia. I've been playing this game since I was a kid, and being an amateur and a student of computer science, I came up with the idea of designing an unbeatable AI for this game. The program named “Humain_Ordinateur” allows a human to play against a computer that makes random moves. The “Ordinateur_Ordinateur” program simulates a random game at En Garde. The program named “Humain_IA” allows a human to play against an AI whose strategy is based on a large number of simulations at each turn to determine the best move using a simple win/loss ratio.

Notes :
- The rules of En Garde are available in pdf format.
- The principle of the first AI is very elementary. An AI using Minimax or MCTS would obviously be more efficient.
- The AI's defense is random in itself, but the possibility of having to defend itself is taken into account in the simulations.
- Coding the AI in C++ instead of Python would allow 26 times more simulations per turn, with the same time.
- I fully respect Reiner Knizia's work and thank him for designing this game. I have no intention of prejudicing him by making En Garde free to access, and in any case, the lack of graphics means that no one may want to use these programs more than twice, and this may even lead to the purchase of the game, which I highly recommend.
- A bonus program called “Assistant” allows a person, playing against someone else in the real board game, to be assisted by the AI. In the program code, you need to enter the hand of the player who wants to be assisted, as well as the discard pile, the positions on the board, and whether the assisted player has the left or right fencer. The rules state that you can't look at the contents of the discard pile, but there's no reason why you shouldn't 🙂.
