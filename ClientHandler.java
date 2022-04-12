import java.io.*;
import java.net.Socket;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Timer;

public class ClientHandler implements Runnable {
    private final ObjectInputStream objectInputStream;
    private final ObjectOutputStream objectOutputStream;

    public ClientHandler(Socket socket) throws IOException {
        InputStream inputStream = socket.getInputStream();
        objectInputStream = new ObjectInputStream(inputStream);
        OutputStream outputStream = socket.getOutputStream();
        objectOutputStream = new ObjectOutputStream(outputStream);
    }

    @Override
    public void run() {
        Runnable save = this::saveNotification;
        Thread saver = new Thread(save);
        saver.start();
    }

    void saveNotification() {
        while(true) {
            try {
                Notification received = (Notification) objectInputStream.readObject();
                DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                System.out.println("[SERVER] Notification received! Msg: " + received.getMsg() + " Time: " +
                        format.format(received.getDate()));
                new Timer().schedule(new SendNotificationTask(received, objectOutputStream), received.getDate());
            } catch (IOException e) {
                System.err.println("Client disconnected");
                break;
            } catch (ClassNotFoundException ignored) {
            }
        }
    }
}