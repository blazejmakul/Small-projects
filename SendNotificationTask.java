import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.TimerTask;

public class SendNotificationTask extends TimerTask {
    Notification notification;
    ObjectOutputStream objectOutputStream;

    public SendNotificationTask(Notification notification, ObjectOutputStream objectOutputStream){
        this.notification = notification;
        this.objectOutputStream = objectOutputStream;
    }

    @Override
    public void run() {
        try {
            objectOutputStream.writeObject(notification);
        } catch (IOException e) {
            System.out.println("[SERVER] Error when sending notification to client");
        }
    }
}
