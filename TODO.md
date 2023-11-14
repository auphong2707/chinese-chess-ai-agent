# This is the task list of the Game Tree Development branch

Tasks: (Note: Check the UML before you do anything)

- [x] 0-000: Create class Node in node.py and initialize it (UML)
- [x] 0-001: Create *generate_all_children* and assign it to *list_of_children* in init function of Node class
- [x] 0-002: Create *uct* property in Node class
- [x] 0-003: Add to the Node class: abstract class, parent, parent_move. Rename *generate_all_children* to *get_all_children*. Remove the UCT property, is_fully_expanded, win_until_now, ters_until_now, parent_iters_until_now, _uct
- [x] 1-001: Create class NodeMinimax inherited from Node. The init function inherited from Node but add 4 more variables: alpha, beta, minimax_value, depth
- [x] 1-002: Create the *generate_all_children* method: This method fill up the *list_of_children*
- [x] 1-003: Create the *reset_statistics* method: This method reset all the value: alpha, beta, minimax_value, depth to -inf, inf, None, None