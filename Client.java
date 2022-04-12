import javax.swing.text.DateFormatter;
import java.io.*;
import java.net.ConnectException;
import java.net.Socket;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Client {
    BufferedReader userinput;
    ObjectOutputStream objectOutputStream;
    ObjectInputStream objectInputStream;

    public static void main(String[] args){
        try{
            Client client = new Client();
            System.out.println("Welcome to NotifyMe System! Please write a message ");
            Runnable receive = client::receiveNotifications;
            Runnable send = client::sendNotification;
            Thread receiver = new Thread(receive);
            Thread sender = new Thread(send);
            receiver.start();
            sender.start();
        }catch(IOException e){
            System.err.println("Couldn't connect to server!");
            System.exit(1);
        }
    }
    public Client() throws IOException{
        Socket socket = new Socket("localhost",7777);
        this.userinput = new BufferedReader(new InputStreamReader(System.in));
        OutputStream outputStream = socket.getOutputStream();
        this.objectOutputStream = new ObjectOutputStream(outputStream);
       InputStream inputStream = socket.getInputStream();
        this.objectInputStream = new ObjectInputStream(inputStream);
    }

    void receiveNotifications(){
        while(true){
            try {
                Notification notification = (Notification) objectInputStream.readObject();
                System.out.println(notification.getMsg());
            } catch (IOException e) {
                System.err.println("Server closed the connection");
                System.exit(0);
            } catch (ClassNotFoundException ignored) {}
        }
    }
    void sendNotification() {
        while(true){
            try {
                System.out.println("New notification... Give message: ");
                String msg = userinput.readLine();
                System.out.println("Give date (yyyy-MM-dd HH:mm:ss):");
                Date date = inputDate();
                Notification notification = new Notification(msg,date);
                objectOutputStream.writeObject(notification);
                System.out.println("Notification sent!");
            } catch (IOException e) {
                System.err.println("Error when creating this notification!");
            }catch(WrongDateException e){
                System.out.println(e.getMsg());
            }
        }

    }
    Date inputDate() throws WrongDateException{
        while(true){
            try{
                DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                String toParse = userinput.readLine();
                Date date = format.parse(toParse);
                Date currDate = new Date(System.currentTimeMillis());
                if(date.before(currDate)){
                    throw new WrongDateException("Given date has already been!",toParse);
                }
                return date;
            }catch(IOException e){
                System.out.println("Wrong input! Try again");
            }catch(ParseException e){
                System.out.println("Wrong date format! Try again");
            }

        }
    }

}
