/**
 * Created by zy9wang on 5/28/2017.
 */
import javafx.util.Pair;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;
public class Brain
{
    public static void main(String args[]) throws IOException {
        Board board = null;
        BufferedReader in  = new BufferedReader(new InputStreamReader(System.in));
        String input = null;
        String stateinput = null;
        Pair<Integer,Integer> move = null;
        while ((input = in.readLine())!= null) {
            String[] inputss = input.split(" ");
            String[] inputs = null;
            if (inputss.length > 1) inputs = inputss[1].split(",");
            switch (inputss[0]){
                case "START": board = new Board(Integer.parseInt(inputs[0]), Integer.parseInt(inputs[0]));System.out.println("OK");break;
                case "END": return;
                case "BEGIN": move = board.goFirst();printMove(move);break;
                case "ABOUT": System.out.println("Bot by Mahuahua, version negative aleph two");break;
                case "TURN": board.place(Integer.parseInt(inputs[0]),Integer.parseInt(inputs[1]),2);move = board.nextPlay();printMove(move);break;
                case "INFO ": break;//ignore limits
                case "RESTART": board.restart();System.out.println("OK");break;
                case "BOARD":
                    while (!(stateinput = in.readLine()).startsWith("DONE")) {
                            String[] stateinputs = stateinput.split(",");
                            board.place(Integer.parseInt(stateinputs[0]),Integer.parseInt(stateinputs[1]),Integer.parseInt(stateinputs[2]));
                    }
                    move = board.nextPlay();
                    printMove(move);
                    break;
                default:
                    break;

            }
        }
    }

    private static void printMove(Pair<Integer,Integer> move){
        System.out.println(move.getKey() + "," + move.getValue());
    }
}
