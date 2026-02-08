# Othello AI Agent – Adversarial Game Tree Search

## Overview  
This project implements an intelligent AI agent for the game Othello (Reversi) using adversarial search techniques. The agent models Othello as a game tree and makes decisions using Minimax and Alpha-Beta pruning under strict time constraints. Multiple optimization techniques are integrated to improve search efficiency and gameplay strength.

The project was developed as a personal AI systems project focused on strategic reasoning, performance optimization, and clean integration with an external game engine.

---

## Game Environment  
- Supports arbitrary board sizes (e.g., 4x4, 6x6, 8x8)  
- Standard Othello rules with disk flipping and legal move constraints  
- Game ends when a player has no legal moves remaining  
- Board represented as immutable tuples for efficient caching  

---

## Core Algorithms

### Minimax Search  
- Recursive Max and Min node evaluation  
- Computes exact utility for terminal states  
- Uses disk count difference as the base utility function  
- Suitable for small board sizes or shallow search depths  

### Alpha-Beta Pruning  
- Optimized adversarial search with pruning  
- Reduces the number of evaluated game states  
- Maintains correctness while significantly improving performance  
- Used as the default search strategy  

---

## Search Optimizations

### Depth-Limited Search  
- Configurable depth limits via command-line flags  
- Uses heuristic evaluation when depth limit is reached  
- Enables scalable play on larger boards  

### State Caching  
- Memoization of evaluated board states  
- Avoids redundant recomputation in deep search trees  
- Improves performance for repeated subtrees  

### Node Ordering  
- Orders successor states by heuristic value  
- Explores higher-utility moves first  
- Increases effectiveness of alpha-beta pruning  

### Heuristic Evaluation  
- Custom heuristic function for non-terminal states  
- Combines disk advantage with board position evaluation  
- Used for depth-limited Alpha-Beta search  
- Includes a documented description directly in the code  

### Implementation Highlights  
- Fully compliant with provided game engine and interfaces  
- No modification of starter code required  
- Uses immutable board representations for safe caching  
- Handles pass moves and terminal game states correctly  
- Designed to operate within a 10-second decision limit  

---

## Usage

Run the Othello GUI against the agent:
```
python3 othello_gui.py -d 6 -a agent.py
```
Enable Minimax:
```
python3 othello_gui.py -d 4 -a agent.py -m
```
Enable depth-limited Alpha-Beta:
```
python3 othello_gui.py -d 6 -a agent.py -l 5
```
Enable caching and node ordering:
```
python3 othello_gui.py -d 8 -a agent.py -c -o -l 5
```
Play AI vs AI:
```
python3 othello_gui.py -d 6 -a agent.py -b randy_ai.py
```

---

## Goals  
- Build a competitive Othello AI using adversarial search  
- Apply Minimax and Alpha-Beta pruning in a real game setting  
- Optimize game tree exploration under time constraints  
- Design and evaluate heuristic functions  
- Demonstrate strategic AI decision-making  

---

## Author
Victoria Piroian  

University of Toronto  

Faculty of Applied Science & Engineering, 2025
