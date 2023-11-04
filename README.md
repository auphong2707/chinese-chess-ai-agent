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
