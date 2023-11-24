# This is the task list of the Game Tree Development branch

Tasks: (Note: Check the UML before you do anything)

- [x] 0-000: Create class Node in node.py and initialize it (UML)
- [x] 0-001: Create *generate_all_children* and assign it to *list_of_children* in init function of Node class
- [x] 0-002: Create *uct* property in Node class
- [x] 0-003: Add to the Node class: abstract class, parent, parent_move. Rename *generate_all_children* to *get_all_children*. Remove the UCT property, is_fully_expanded, win_until_now, ters_until_now, parent_iters_until_now, _uct
- [x] 1-001: Create class NodeMinimax inherited from Node. The init function inherited from Node but add 4 more variables: alpha, beta, minimax_value, depth
- [x] 1-002: Create the *generate_all_children* method: This method fill up the *list_of_children*
- [x] 1-003: Create the *reset_statistics* method: This method reset all the value: alpha, beta, minimax_value, depth to -inf, inf, None, None
- [x] 2-000: Create abstract class GameTree in game_tree.py. Add 2 methods: *move_to_best_child* and *move_to_child_node_with_move*
- [x] 2-001: Add the method *is_lost* return True if the GameTree (bot) is lost
- [x] 3-000: Create GameTreeMinimax class inherited from GameTree class. Add the *minimax* method to it
- [x] 3-001: Fix the alpha-beta pruning and target-depth of the GameTreeMinimax
- [x] 3-002: Change the depth target to the instance variable
- [x] 4-000: Create NodeMCTS inherited from Node and initialize it. Create the *generate_all_unvisited_node* method
- [ ] 4-001: Create *rollout*, *backpropagate*, *best_child* method in NodeMTCS
- [x] 5-000: Create UI of the GameTree
- [ ] 5-001: Create Main menu with 2 modes: Bot vs Bot and Human vs Bot. Add the interactive to the UI
- [ ] 6-000: Create GameTreeMCTS and add all the needed method into it
