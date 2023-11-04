# Chinese chess AI agent
This is the project about creating a simple AI game engine for Chinese chess

## Theory
### Minimax algorithm
#### Overview:
The Minimax algorithm is a decision-making algorithm used in artificial intelligence, decision theory, game theory, statistics, and philosophy. In a two-player game such as chess, it determines the optimal move for a player by minimizing the possible loss for a worst-case (maximum loss) scenario. It has also been extended to more complex games and general decision-making in the presence of uncertainty.
#### Full description:
#### Complexity:
- Time complexity: $O(b^d)$
- Space complexity: $O(bd)$
#### Psuedocode:
```
GLOBAL INF

FUNCTION minimax (node_index, node_depth, max_turn, target_depth, value)
    // If the node reaches the target depth
    IF node_depth == target_depth THEN
        RETURN value[node_index]
        
    // If this turn is to find the maximum
    IF max_turn == TRUE THEN
        result = -INF    // Initialize the result value as negative infinity

        // Iterate over children of the node and update the result
        FOR child_index IN child_list[node_index]
            result = MAX(result, minimax(child_index, node_depth + 1, FALSE, target_depth, value))

        RETURN result    // Return the result
        
    // If this turn is to find the minimum
    ELSE
        result = INF    // Initialize the result value as positive infinity

        // Iterate over children of the node and update the result
        FOR child_index IN child_list[node_index]
            result = MIN(result, minimax(child_index, node_depth + 1, TRUE, target_depth, value))

        RETURN result    // Return the result
ENDFUNCTION
```
### Alpha-beta pruning
#### Overview:
Alpha-beta pruning is a search technique which aims to reduce the number of nodes in its search tree that are evaluated by the minimax algorithm. This adversarial search technique is frequently used for computer play of two-player combinatorial games (Chess, Tic Tac Toe, etc.). When used on a typical minimax tree, it produces the same move as minimax but removes branches that are unable to affect the final choice.
#### Full description:
#### Complexity:
- Time complexity: $O(\sqrt{b^d})$
- Space complexity: $O(bd)$
#### Psuedocode:
```
GLOBAL INF

FUNCTION minimax (node_index, node_depth, max_turn, target_depth, value, alpha, beta)
    // If the node reaches the target depth
    IF node_depth == target_depth THEN
        RETURN value[node_index]

    // If this turn is to find the maximum
    IF max_turn == TRUE THEN
        result = -INF     // Initialize the result value as negative infinity

        // Iterate over children of the node
        FOR child_index IN child_list[node_index]
            // Get the evaluation value of the child node
            value = minimax(node_index, node_depth + 1, FALSE, target_depth, value, alpha, beta)
            
            result = MAX(result, value)    // Update result
            alpha = MAX(alpha, result)    // Update alpha value of the node
            IF beta <= alpha THEN    // When stop condition invokes, stop the iteration
                BREAK
        RETURN result

    // If this turn is to find the minimum
    ELSE
        result = +INF    // Initialize the result value as negative infinity

        // Iterate over children of the node
        FOR child_index IN child_list[node_index]
            // Get the evaluation value of the child node
            value = minimax(node_index, node_depth + 1, TRUE, target_depth, value, alpha, beta)

            result = MIN(result, value)    // Update result
            beta = MIN(beta, result)    // Update alpha value of the node
            IF beta \\<= alpha THEN    // When stop condition invokes, stop the iteration
                BREAK
        RETURN result
ENDFUNCTION
```
### Monte Carlo Tree Search
