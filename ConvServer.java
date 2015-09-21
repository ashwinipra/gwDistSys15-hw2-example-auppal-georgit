/*
 * Ahsen Uppal
 * and
 * Teo Georgiev
 */

/******************************************************************************
 *
 *  CS 6421 - Simple Conversation
 *  Compilation:  javac ConvServer.java
 *  Execution:    java ConvServer port [unit1 unit2 scale]
 *
 *  % java ConvServer portnum [unit1 unit2 scale]
 *
 * By default, this program runs a ft to in conversion server, but
 * with optional command-line arguments, it can run as any conversion
 * server.
 *
 ******************************************************************************/

import java.net.Socket;
import java.net.ServerSocket;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.UnknownHostException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class ConvServer {

    public static void process (Socket clientSocket, String unit1, String unit2, float scale) throws IOException {
        // open up IO streams
        BufferedReader in = new BufferedReader(new
InputStreamReader(clientSocket.getInputStream()));
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(),
true);

        /* Write a welcome message to the client */
        out.println("Welcome, you are connected to a Java-based server");

        /* read and print the client's request */
        // readLine() blocks until the server receives a new line from client
        String userInput;
        if ((userInput = in.readLine()) == null) {
            System.out.println("Error reading message");
            out.close();
            in.close();
            clientSocket.close();
        }

        System.out.println("Received message: " + userInput);

        String[] inputs = userInput.split(" ");
        if (inputs.length != 3)
        {
            System.out.println("Couldn't convert that - use format \'unit1 unit2 number\'");
        }

        double number = Float.parseFloat(inputs[2]);

        double answer;
        if (inputs[0].equals(unit1) && inputs[1].equals(unit2))
        {
            answer = number * scale;
            System.out.println(answer);
            out.println(answer);
        }
        else
        {
            String msg = "This server can only convert " + unit1 + " to " + unit2;
            System.out.println(msg);
            out.println(msg);
        }

        // close IO streams, then socket
        out.close();
        in.close();
        clientSocket.close();
    }

    public static void main(String[] args) throws Exception {
        String unit_src = "ft";
        String unit_dst = "in";
        float scale = 12;

        //check if argument length is invalid
        if (args.length < 1) {
            System.err.println("Usage: java ConvServer port [unit1 unit2 scale]");
        }

        // create socket
        int port = Integer.parseInt(args[0]);

        if (args.length > 3) {
            unit_src = args[1];
            unit_dst = args[2];
            scale = Float.parseFloat(args[3]);
        }

        ServerSocket serverSocket = new ServerSocket(port);
        System.err.println("Started Java-based " + unit_src + " to " + unit_dst + " conversion server on port " + port);

        // wait for connections, and process
        try {
            while(true) {
                // a "blocking" call which waits until a connection is requested
                Socket clientSocket = serverSocket.accept();
                System.err.println("\nAccepted connection from client");
                process(clientSocket, unit_src, unit_dst, scale);
            }

        }catch (IOException e) {
            System.err.println("Connection Error");
        }
        System.exit(0);
    }
}
