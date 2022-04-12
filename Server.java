import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server {
    private ArrayList<ClientHandler> clients = new ArrayList<>();
    private ExecutorService pool = Executors.newFixedThreadPool(10);

    public static void main(String[] args){
        Server server = new Server();
        try{
            ServerSocket listen = new ServerSocket(7777);
            while(true){
                System.out.println("[SERVER] Waiting for client to connect...");
                Socket listener = listen.accept();
                System.out.println("[SERVER] Connection established with new client!");
                ClientHandler client = new ClientHandler(listener);
                server.clients.add(client);
                server.pool.execute(client);
            }
        } catch (IOException e) {
            System.err.println("Error on establishing a new connection");
        }


    }
}
