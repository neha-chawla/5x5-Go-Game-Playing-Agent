# Go Game-Playing Agent

Objective: Develop AI agents based on some of the AI techniques for Search, Game Playing, and Reinforcement Learning to play a small version of the Go game, called Go-5x5 or Little-Go, that has a reduced board size of 5x5. 

Rules: Go is an abstract strategy board game for two players, in which the aim is to surround more territory than the opponent. The basic concepts of Go (Little-Go) are very simple:

- Players: Go is played by two players, called Black and White.
- Board: The Go board is a grid of horizontal and vertical lines. The standard size of the board is 19x19, but in this homework, the board size will be 5x5.
- Point: The lines of the board have intersections wherever they cross or touch each other. Each intersection is called a point. Intersections at the four corners and the edges of the board are also called points. Go is played on the points of the board, not on the squares.
- Stones: Black uses black stones. White uses white stones.

Gameplay: 
- It starts with an empty board,
- Two players take turns placing stones on the board, one stone at a time,
- The players may choose any unoccupied point to play on (except for those forbidden by the “KO” and “no-suicide” rules).
- Once played, a stone can never be moved and can be taken off the board only if it is captured.
- The entire game of Go (Little-Go) is played based on two simple rules: Liberty (No-Suicide) and KO.

The image below shows the basic program structure. There is one game host and two players in each game. The Game Host keeps track of the game process, gets the next moves from the players in turn, judges if the proposed moves are valid, wipes out the dead stones, and finally judges the winner. Each of the two Players must output its next move in an exact given format (in a file called output.txt) with the intended point (row and column) coordinates to the Game Host. The job of a player is very simple: take the previous and current states of the board (in a file called input.txt) from the host, and then output the next move back to the host.input) from the host, and then output the next move back to the host.

<img width="366" alt="Screenshot 2024-11-25 at 4 26 56 PM" src="https://github.com/user-attachments/assets/babc5030-a6f3-4151-b4fb-728a8104e408">

The host keeps track of the game board while the two players make moves in turn. We will use a zero-based, vertical-first, start at the top-left indexing in the game board. So, location [0,0] is the top-left corner of the board, location [0,4] is the top-right corner, location [4,0] is the bottom-left corner, and location [4,4] is the bottom-right corner. An example of game state is shown in Figure 2, in which "1" denotes black stones, "2" denotes white stones, and "0" denotes empty positions. For manual players, we visualize the board as in the image on the right where X denotes the black stones and O denotes the white stones.

<img width="519" alt="Screenshot 2024-11-25 at 4 28 28 PM" src="https://github.com/user-attachments/assets/6eb10747-d185-422f-be9d-ab53f4657278">

AI Players
The agent was tested against different AI players such as:
- Random Player: Moves randomly.
- Greedy Player: Places the stone that captures the maximum number of enemy stones
- Aggressive Player: Looks at the next two possible moves and tries to capture the maximum number of enemy stones.
- Alphabeta Player: Uses the Minimax algorithm (Depth<=2; Branching factor<=10) with alpha-beta pruning.
- QLearningPlayer: Uses Q-Learning to learn Q values from practice games and make moves intelligently under different game conditions.
- Championship Player: This is an excellent Little-Go player adapted from past top-performing agents.

Results:
My agent (Minimax algorithm with alpha-beta pruning) beats the Random, Greedy, Aggressive, Alphabeta, and QLearning players 10/10 times. Against the Championship player, my agent wins 6/10 times.
