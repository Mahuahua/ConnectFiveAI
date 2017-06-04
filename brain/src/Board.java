import javafx.util.Pair;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

/**
 * Created by zy9wang on 5/28/2017.
 */
public class Board {
    int[][] state = null;
    int width = 0, height = 0, count = 0;

    public Board(int width, int height) {
        state = new int[width][height];
        this.width = width;
        this.height = height;
        this.count = 0;
    }

    public Pair<Integer, Integer> goFirst() {
        state[width / 2][height / 2] = 1;
        return new Pair<>(width / 2, height / 2);
    }


    private HashSet<Pair<Integer, Integer>> getValuableMoves(int range) {
        HashSet<Pair<Integer, Integer>> valuablesMoves = new HashSet<>();
        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                if (state[i][j] == 0) {
                    boolean foundInRange = false;
                    for (int k = -range; k <= range && !foundInRange; k++) {
                        for (int l = -range; l <= range && !foundInRange; l++) {
                            if (i + k >= 0 && i + k < width && j + l >= 0 && j + l < height && state[i + k][j + l] != 0) {
                                foundInRange = true;
                                valuablesMoves.add(new Pair<Integer, Integer>(i, j));
                            }
                        }
                    }
                }
            }
        }

        return valuablesMoves;
    }

    private final int[] BLOCKBOTH = {0,0, 0, 0, 0, 9999999};
    private final int[] BLOCKONE = {0,1, 12, 30, 120, 9999999};
    private final int[] FREE = {0,2, 25, 500, 99999, 9999999};

    private int getScore(boolean blockStart, boolean blockEnd, int k) {
        if (k > 5) k = 5;
        if (blockStart && blockEnd) return BLOCKBOTH[k];
        else if (!blockStart && !blockEnd) return FREE[k];
        else return BLOCKONE[k];
    }

    private double calculateScore(int team) {

        double finalScore = 0;
        //other numbers are also used
        int otherTeam = 1;
        if (team == 1) otherTeam = 2;


        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                if (state[i][j] == team) {
                    boolean blockStart, blockEnd;
                    int k;
                    //only consider scoring if i,j is the start of a sequence
                    if (i - 1 < 0 || state[i - 1][j] != team) {
                        blockStart = i - 1 < 0 || state[i - 1][j] == otherTeam;
                        k = 1;
                        while (i + k < width && state[i + k][j] == team) k++;
                        blockEnd = i + k >= width || state[i + k][j] == otherTeam;
                        if (i + k - 6 < 0 || i + 5 > width) {
                            //if boarder encountered, no points
                        } else {
                            finalScore = finalScore + getScore(blockStart, blockEnd, k);
                        }
                    }

                    if (j - 1 < 0 || state[i][j - 1] != team) {
                        blockStart = j - 1 < 0 || state[i][j - 1] == otherTeam;
                        k = 1;
                        while (j + k < height && state[i][j + k] == team) k++;
                        blockEnd = j + k >= height || state[i][j + k] == otherTeam;
                        if (j + k - 6 < 0 || j + 5 > height) {
                            //if boarder encountered, no points
                        } else {
                            finalScore = finalScore + getScore(blockStart, blockEnd, k);
                        }
                    }

                    if (i - 1 < 0 || j - 1 < 0 || state[i - 1][j - 1] != team) {
                        blockStart = i - 1 < 0 || j - 1 < 0 || state[i - 1][j - 1] == otherTeam;
                        k = 1;
                        while (j + k < height && i + k < width && state[i + k][j + k] == team) k++;
                        blockEnd = j + k >= height || i + k >= width || state[i + k][j + k] == otherTeam;
                        if (j + k - 6 < 0 || j + 5 > height || i + k - 6 < 0 || i + 5 > width) {
                            //if boarder encountered, no points
                        } else {
                            finalScore = finalScore + getScore(blockStart, blockEnd, k);
                        }
                    }

                    if (i + 1 >= width || j - 1 < 0 || state[i + 1][j - 1] != team) {
                        blockStart = i + 1 >= width || j - 1 < 0 || state[i + 1][j - 1] == otherTeam;
                        k = 1;
                        while (j + k < height && i - k >= 0 && state[i - k][j + k] == team) k++;
                        blockEnd = j + k >= height || i - k < 0 || state[i - k][j + k] == otherTeam;
                        if (j + k - 6 < 0 || j + 5 > height || i - 6 < 0 || i - k + 5 > width) {
                            //if boarder encountered, no points
                        } else {
                            finalScore = finalScore + getScore(blockStart, blockEnd, k);
                        }
                    }


                }
            }
        }
        return finalScore;

    }

    private double calculateOppoScore() {
        HashSet<Pair<Integer, Integer>> moves = getValuableMoves((int)Math.round((count+1)*4.0/width/height +1));
        double maxScore = 0;
        double avg = 0; //for case of first move when going second, better place something beside first piece
        for (Pair<Integer, Integer> move : moves) {
            state[move.getKey()][move.getValue()] = 2;
            double score = calculateScore(2);
            state[move.getKey()][move.getValue()] = 0;
            avg = avg + score;
            if (score > maxScore) {
                maxScore = score;
            }

        }
        return maxScore + avg / moves.size() / 30; //avg have a 1/30 influence
    }

    public Pair<Integer, Integer> nextPlay() {
        count++;
        HashSet<Pair<Integer, Integer>> moves = getValuableMoves((int)Math.round(count*4.0/width/height +1));




        double maxScore = -99999999;
        Pair<Integer, Integer> bestPair = new Pair<>(0, 0);

        for (Pair<Integer, Integer> move : moves) {
            state[move.getKey()][move.getValue()] = 1;
            double selfScore = calculateScore(1);
            double oppoNextBestScore = calculateOppoScore();
            state[move.getKey()][move.getValue()] = 0;
            if (selfScore - 0.92 * oppoNextBestScore > maxScore) {
                maxScore = selfScore - 0.92 * oppoNextBestScore;
                bestPair = move;
            }
        }

        state[bestPair.getKey()][bestPair.getValue()] = 1;
        return bestPair;
    }

    public void restart() {
        state = new int[width][height];
        count = 0;
    }

    public void place(int x, int y, int z) {
        state[x][y] = z; count++;
    }
}
