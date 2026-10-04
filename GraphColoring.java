/*
 * DAA Macro Project - Unit IV : Backtracking
 * Project <No> : Graph Coloring (4 vertices, m = 3 colors) with State Space Tree tracing
 *
 * Idea : color ONE vertex at a time, from vertex A onwards. For every vertex try each
 *        color (R, G, B) left to right. A color is SAFE if no already-colored neighbor
 *        has the same color. If a vertex has no safe color, BACKTRACK: remove the
 *        previous vertex's color and try its next color.
 *
 * Every isSafe() test corresponds to one node of the state space tree
 * (root + one node per attempted coloring). Unsafe nodes are pruned (red in the chart).
 *
 * Graph : K4 (every pair of vertices adjacent), so no valid 3-coloring exists and the
 *         trace shows the maximum amount of backtracking.
 *
 * Build : javac GraphColoring.java
 * Run   : java GraphColoring
 */
import java.util.Arrays;

public class GraphColoring {

    static final String[] VERTICES = {"A", "B", "C", "D"};
    static final String[] COLORS = {"R", "G", "B"};

    // Adjacency matrix for K4 (every pair of vertices is adjacent)
    static final int[][] GRAPH = {
        {0, 1, 1, 1},
        {1, 0, 1, 1},
        {1, 1, 0, 1},
        {1, 1, 1, 0}
    };

    // assignment[v] = color index of vertex v, or -1 if uncolored
    static int[] assignment = new int[VERTICES.length];

    // A color is safe if no already-colored neighbor uses it
    static boolean isSafe(int v, int c) {
        for (int u = 0; u < VERTICES.length; u++) {
            if (GRAPH[v][u] == 1 && assignment[u] == c) {
                return false;
            }
        }
        return true;
    }

    static boolean colorGraph(int v) {
        if (v == VERTICES.length) {              // all vertices colored
            return true;
        }
        String indent = "  ".repeat(v);
        for (int c = 0; c < COLORS.length; c++) {
            if (isSafe(v, c)) {
                assignment[v] = c;
                System.out.println(indent + "ASSIGN    " + VERTICES[v] + " = " + COLORS[c]);
                if (colorGraph(v + 1)) {
                    return true;
                }
                assignment[v] = -1;               // undo choice (BACKTRACK)
                System.out.println(indent + "BACKTRACK " + VERTICES[v] + " = " + COLORS[c] + " removed");
            } else {
                System.out.println(indent + "CONFLICT  " + VERTICES[v] + " = " + COLORS[c] + " not allowed");
            }
        }
        return false;                             // no color works, go back
    }

    public static void main(String[] args) {
        Arrays.fill(assignment, -1);
        boolean ok = colorGraph(0);
        System.out.println();
        if (ok) {
            StringBuilder sb = new StringBuilder("Result: ");
            for (int i = 0; i < VERTICES.length; i++) {
                sb.append(VERTICES[i]).append("=").append(COLORS[assignment[i]]).append(" ");
            }
            System.out.println(sb.toString().trim());
        } else {
            System.out.println("Result: No valid 3-coloring exists");
        }
    }
}