import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

import org.chocosolver.solver.exception.ContradictionException;

public class Main {

	public static void main(String[] args) throws IOException, ContradictionException {
		// TODO Auto-generated method stub
		PrintStream o;

		SR sr;
		int[] all_sizes = {20, 40, 60, 80, 100, 150, 200};
		List<Integer> sizes = new LinkedList<Integer>();
		for (int size : all_sizes) {
			if (size >= Integer.parseInt(args[2]) && size <= Integer.parseInt(args[3]))
				sizes.add(size);
		}
		int[] densities = {25, 50, 75, 100};
		String base;
		if (args[0].equals("default"))
			base ="C:\\Users\\Sofia\\Documents\\level5project\\SRI_IP\\data\\";
		else
			base = args[0];
		Path in = Paths.get(base, "instances");
		String criteria = args[1];
		String[] valid_criteria = new String[] {"egal", "1stmax", "rankmax", "generous", "almost"};
		if (!Arrays.asList(valid_criteria).contains(criteria))
			throw new IllegalArgumentException(criteria + " is not a valid criteria!");
		Path outfolder = Paths.get(base, "outputs", "CP_new", criteria + "-SRI");
		File fold = new File(outfolder.toString());
		String path;
		fold.mkdirs();
		for (int size : sizes) {
			for (int density : densities) {
				o = new PrintStream(
						new File(
								outfolder.resolve(
										"output" + "-" + criteria + "-" + size + "-" + density + ".txt").toString()));
				System.setOut(o); 
				for (int i = 1; i <= 20; i++) {
					System.out.println("\nSearch ended");
					path = in.resolve(Paths.get(size + "", "i-" + size + "-" + density + "-" + i + ".txt")).toString();
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
