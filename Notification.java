import java.io.Serializable;
import java.util.Date;

public class Notification implements Serializable{
    final private String msg;
    final private Date date;
    public Notification(String msg, Date date) {
        this.msg = msg;
        this.date = date;
    }
    public String getMsg() {
        return msg;
    }
    public Date getDate() {
        return date;
    }
}
