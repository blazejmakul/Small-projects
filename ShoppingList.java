import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.io.*;

class Program{
	public static void main(String[] argss){
		Program main = new Program(); //dzieki temu nie musisz miec staticow
		ShoppingList shoppingList = new ShoppingList(); // Tu inicjalizuję klasę ShoppingList nazywając ją shoppingList aby móc korzystać z jej metod
		System.out.println("***Loading your shopping list from a file...***");
		shoppingList.load(); //Linia 109
		main.menu(shoppingList); // przekazuję obiekt shoppingList stworzony w lini 9 aby metoda menu mogła z niego dalej korzystać
		System.exit(0);
	}

	void menu(ShoppingList shoppingList){
		while(true){
			printMenu();
			int opt = userChoice();
			switch(opt){
				case 0:
					shoppingList.save();
					System.exit(0);
				case 1: 
					shoppingList.add();
					break;
				case 2:
					shoppingList.remove();
					break;
				case 3:
					shoppingList.clear();
					System.out.println("List has been cleared");
					break;
				case 4:
					shoppingList.save();
					System.out.println("File saved!");
					break;
				default:
					System.out.println("Wrong option!");
					break;
			}
		}
	}	
	void printMenu(){
		System.out.println("Choose what you want to do next:");
		System.out.println("(1) Add item to list");
		System.out.println("(2) Remove item from list");
		System.out.println("(3) Remove all items from list");
		System.out.println("(4) Save current list to drive");
		System.out.println("(0) Exit");
	}
	int userChoice(){
		Scanner input = new Scanner(System.in);
			String ip = input.nextLine();
			int opt = 0;
			try {
				opt = Integer.parseInt(ip);
			} 
			catch (NumberFormatException e) {
				opt=-1;
			}
			return opt;
	}
}

class ShoppingList{
	List<Category> Categories = new ArrayList<Category>();
	
	int findIndex(List<Category>Categories, String category){
		int index = 0;
		while(index < Categories.size()){
			if(Categories.get(index).name.equals(category))
				break;
			index++;
		}
		return index;
	}
	void add(){
		Scanner input = new Scanner(System.in);
		System.out.println("Category:");
		String category = input.nextLine();
		int index = findIndex(Categories, category);
		if(index == Categories.size()){
			Category temp = new Category(category);
			Categories.add(temp);
		}
		System.out.println("Item:");
		String item = input.nextLine();
		Categories.get(index).addItem(item);
		System.out.println("Item added!");
	}
	void remove(){
		Scanner input = new Scanner(System.in);
		System.out.println("Category of item to remove:");
		String catname = input.nextLine();
		int index = findIndex(Categories, catname);
		System.out.println("Item to remove:");
		String item = input.nextLine();
		Categories.get(index).removeItem(item);
		System.out.println("Item removed!");
	}
	void clear(){
		Categories.clear();
	}
	void save(){
		FileHandler fh = new FileHandler();
		fh.saveFile(Categories);
	}
	void load(){
		FileHandler filehandler = new FileHandler();
		try{
			Categories = filehandler.readFile(Categories);
			System.out.println("Loading sucessfull!");
		}catch(FileNotFoundException e){
			System.out.println("File not found!");
			filehandler.saveFile(Categories);
		}
	}
}

class FileHandler{
	void saveFile(List<Category> Categories){
		try{
			File f= new File("ShoppingList.txt");
			f.delete();
			f.createNewFile();
			FileWriter writer = new FileWriter("ShoppingList.txt");		
			int i=0,j=0;
			while(i < Categories.size()){
				j=0;
				writer.write("-" + Categories.get(i).name + "\n");
				while(j < Categories.get(i).Items.size()){
					writer.write(Categories.get(i).Items.get(j) + "\n");
					j++;
				}
				i++;
			}
			writer.close();
		}catch(IOException e){
			e.printStackTrace();
		}		
	}
	List<Category> readFile(List<Category> Categories)throws FileNotFoundException{
		BufferedReader reader;
		try{
			reader = new BufferedReader(new FileReader("ShoppingList.txt"));
			String line = reader.readLine();
			int i = -1;
			while (line != null) {
				if (line.charAt(0) == '-'){
					Category temp = new Category(line.substring(1));
					Categories.add(temp);
					i++;
				}
				else if(line.charAt(0) == '%') continue;
				else{
					Categories.get(i).addItem(line);
				}
				line = reader.readLine();
			}
			reader.close();
			return Categories;
		}catch (IOException e) {
			throw new FileNotFoundException();
		}
	}
}

class Category{
	String name;
	ArrayList<String> Items = new ArrayList<String>();
	public Category(String str){
		name = str;
	}
	public void addItem(String item){
		Items.add(item);
	}
	public void removeItem(String item){
		Items.remove(item);
	}
}