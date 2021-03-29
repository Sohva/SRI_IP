import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;

import org.chocosolver.solver.exception.ContradictionException;

public class Main {

	public static void main(String[] args) throws IOException, ContradictionException {
		// TODO Auto-generated method stub
		PrintStream o;

		SR sr;
		int[] sizes = {20};
		int[] densities = {75};
		String base = "C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\";
		String out = "outputs\\CP_new";
		String in = "instances\\";
		String criteria = "almost";
		String folder = base + out + "\\" + criteria  + "-SRI\\";
		File fold = new File(folder);
		String path;
		fold.mkdirs();
		for (int size : sizes) {
			for (int density : densities) {
				o = new PrintStream(
						new File(
								folder + "output" + "-" + criteria + "-" + size + "-" + density + ".txt"));
				System.setOut(o); 
				for (int i = 1; i <= 20; i++) {
					System.out.println("\nInstance");
					path = base + in + size + "\\i-" + size + "-" + density + "-" + i + ".txt";
					if (criteria.equals("rankmax") || criteria.equals("generous")) {
						SR.solveProfile(path, criteria);
					}
					else {
						sr = new SR(path);
						sr.build(criteria);
						sr.solve("optimise");
						sr.stats();
					}
				}

			}
		}

	}

}
