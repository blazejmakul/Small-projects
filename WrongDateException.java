public class WrongDateException extends Exception{
    private final String msg;
    private final String date;

    public WrongDateException(String msg, String date){
        this.msg = msg;
        this.date = date;
    }

    public String getDate() {
        return date;
    }

    public String getMsg() {
        return msg;
    }
}
