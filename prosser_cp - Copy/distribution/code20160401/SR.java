
//
// Toolkit constraint encoding
//
import java.io.*;
import java.util.*;

import org.chocosolver.solver.Model;
import org.chocosolver.solver.Solution;
import org.chocosolver.solver.Solver;
import org.chocosolver.solver.exception.ContradictionException;
import org.chocosolver.solver.variables.BoolVar;
import org.chocosolver.solver.variables.IntVar;
import org.chocosolver.util.iterators.DisposableValueIterator;
import org.chocosolver.util.tools.ArrayUtils;
import org.chocosolver.solver.search.strategy.Search;

public class SR {

	int n;
	int[][] rank; // rank[i][j] = k <-> agent_i ranks agent_j as k^th choice
	int[][] pref; // pref[i][k] = j <-> agent_i has agent_j as k^th choice
	int[] length; // length of agent's preference list
	Model model;
	Solver solver;
	IntVar[] agent; // domain of ranks, last is unmatched

	// Optimisation variables
	IntVar cost;
	IntVar[] profile;
	IntVar[][] blocking;
	IntVar blocking_sum;
	
	long totalTime, modelTime, solveTime, readTime, modelSize;
	boolean search;
	int solutions, matchingSize;

	SR(String fname) throws IOException {
		search = true;
		totalTime = System.currentTimeMillis();
		readTime = System.currentTimeMillis();
		read(fname);
		readTime = System.currentTimeMillis() - readTime;
	}

	SR(SMSRInstance inst) {
		search = true;
		totalTime = System.currentTimeMillis();
		readTime = System.currentTimeMillis();
		read(inst);
		readTime = System.currentTimeMillis() - readTime;
	}

	void read(String fname) throws IOException {
		BufferedReader fin = new BufferedReader(new FileReader(fname));
		n = Integer.parseInt(fin.readLine());
		pref = new int[n][n];
		rank = new int[n][n];
		length = new int[n];
		for (int i = 0; i < n; i++) {
			StringTokenizer st = new StringTokenizer(fin.readLine(), " ");
			int k = 0;
			length[i] = 0;
			while (st.hasMoreTokens()) {
				int j = Integer.parseInt(st.nextToken()) - 1;
				rank[i][j] = k;
				pref[i][k] = j;
				length[i] = length[i] + 1;
				k = k + 1;
			}
			rank[i][i] = k;
			pref[i][k] = i;
		}
		fin.close();
	}

	void read(SMSRInstance inst) {
		n = inst.n;
		pref = new int[n][n];
		rank = new int[n][n];
		length = new int[n];
		for (int i = 0; i < n; i++) {
			int k = 0;
			length[i] = 0;
			for (int j : (ArrayList<Integer>) inst.pref[i]) {
				rank[i][j] = k;
				pref[i][k] = j;
				length[i] = length[i] + 1;
				k = k + 1;
			}
			rank[i][i] = k;
			pref[i][k] = i;
		}
	}

	void build(String command, int maximise, int[] minProfile) {
		modelTime = System.currentTimeMillis();
		model = new Model();
		agent = model.intVarArray("agents", n, 0, n - 1);
		if (command.equals("almost")) {
			blocking = model.intVarMatrix(n, n, 0, 1);
			blocking_sum = model.intVar(0, n*n);
		}
		for (int i = 0; i < n; i++)
			for (int j = 0; j < length[i]; j++) {
				int k = pref[i][j];
				if (!command.equals("almost")) {
					model.ifThen(model.arithm(agent[i], ">", rank[i][k]), model.arithm(agent[k], "<", rank[k][i]));
				} else {
					model.ifThen(model.arithm(agent[i], ">", rank[i][k]),
							model.or(model.arithm(agent[k], "<", rank[k][i]),
									model.arithm(blocking[i][k], "=", 1)));
				}
				model.ifThen(model.arithm(agent[i], "=", rank[i][k]), model.arithm(agent[k], "=", rank[k][i]));
			}
		if (command.equals("egal")) {
			cost = model.intVar("cost", 0, n * (n - 1));
			model.sum(agent, "=", cost).post();
			model.setObjective(Model.MINIMIZE, cost);
		}
		if (command.equals("almost")) {
			model.sum(ArrayUtils.flatten(blocking), "=", blocking_sum).post();
			model.setObjective(Model.MINIMIZE, blocking_sum);
		}
		if (command.equals("1stmax") || command.equals("rankmax") || command.equals("generous")) {
			profile = model.intVarArray("profile", n, 0, n);
			for (int i = 0; i < n; i++) {
				model.count(i, agent, profile[i]).post();
			}
			for (int i = 0; i < minProfile.length; i++) {
				if (command.equals("generous"))
					model.arithm(profile[minProfile.length - i - 1], "<=", minProfile[minProfile.length - i - 1]).post();
				else
					model.arithm(profile[i], ">=", minProfile[i]).post();
			}
			if (command.equals("generous"))
				model.setObjective(Model.MINIMIZE, profile[maximise]);
			else
				model.setObjective(Model.MAXIMIZE, profile[maximise]);
		}
		solver = model.getSolver();
		if (command.equals("almost")) {
			//solver.setSearch(Search.minDomLBSearch(agent));
			solver.setSearch(Search.activityBasedSearch(ArrayUtils.append(
					ArrayUtils.flatten(blocking), agent, new IntVar[] {blocking_sum})));
		}
		
		modelTime = System.currentTimeMillis() - modelTime;
		modelSize = (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1024; // kilobytes
	}

	void build(String command) {
		build(command, 0, new int[] {});
	}

	Solution solveProfileIteration(int i) throws ContradictionException {
		Solution solution = new Solution(model);
		while (solver.solve()) {
			solution.record();
			solutions += 1;
		}
		if (solutions > 0) {
			return solution;
		}
		else return null;
	}

	static void solveProfile(String path, String criteria) throws ContradictionException, IOException {
		long totalTime = System.currentTimeMillis();
		SR sr = new SR(path);
		int[] minProfile = new int[sr.n];
		for (int i = 0; i < minProfile.length; i++) {
			if (criteria.equals("generous"))
				minProfile[i] = sr.n;
			else
				minProfile[i] = 0;
		}
		Solution solution = null;
		int solutions = 0;
		int index;
		for (int i = 0; i < sr.n - 1; i++) {
			if (criteria.equals("generous")) index = sr.n - 1 - i;
			else index = i;
			sr.build(criteria, index, minProfile);
			solution = sr.solveProfileIteration(index);
			if (solution == null) break;
			minProfile[index] = solution.getIntVal(sr.profile[index]);
		}
		if (solution != null) {
			sr.getMatchingSize(solution);
			sr.displayMatching(solution);	
			solutions = 1;
		}
		System.out.print("solutions: " + solutions + " ");
		System.out.print("totalTime: " + (System.currentTimeMillis() - totalTime) + "  \n");
	}

	void solve(String command) throws ContradictionException {
		solutions = matchingSize = 0;
		solveTime = System.currentTimeMillis();
		// solver.setVarIntSelector(new StaticVarOrder(solver,solver.getVar(agent)));
		if (command.equals("count")) { // count all solutions
			while (solver.solve()) {
				solutions += 1;
			}
			if (solutions > 0)
				matchingSize = getMatchingSize();
		} else if (command.equals("all")) { // enumerate all solutions
			while (solver.solve()) {
				getMatchingSize();
				displayMatching();
			}
		} else if (command.equals("propagate")) {
			search = false;
			solver.propagate();
			try {
				solver.propagate();
				displayPhase1Table();
			} catch (ContradictionException e) {
				displayPhase1Table();
			}
		} else if (command.equals("optimise")) {
			Solution solution = new Solution(model);
			while (solver.solve()) {
				solution.record();
				solutions += 1;
			}
			if (solutions > 0) {
				getMatchingSize(solution);
				displayMatching(solution);
			}
		}
		else if (solver.solve()) {
			solutions = 1;
			getMatchingSize();
			displayMatching();
		}
		solveTime = System.currentTimeMillis() - solveTime;
		totalTime = System.currentTimeMillis() - totalTime;
	}

	int getMatchingSize() {
		matchingSize = 0;
		for (int i = 0; i < n; i++)
			if (agent[i].getValue() < length[i])
				matchingSize++;
		matchingSize = matchingSize / 2;
		return matchingSize;
	}

	int getMatchingSize(Solution s) {
		matchingSize = 0;
		for (int i = 0; i < n; i++)
			if (s.getIntVal(agent[i]) < length[i])
				matchingSize++;
		matchingSize = matchingSize / 2;
		return matchingSize;
	}


	void displayMatching() {
		for (int i = 0; i < n; i++) {
			int j = pref[i][agent[i].getValue()];
			if (i < j)
				System.out.print("(" + (i + 1) + "," + (j + 1) + ") ");
		}
		System.out.println();
	}

	void displayMatching(Solution s) {
		for (int i = 0; i < n; i++) {
			int j = pref[i][s.getIntVal(agent[i])];
			if (i < j)
				System.out.print("(" + (i + 1) + "," + (j + 1) + ") ");
		}
		System.out.println();
	}

	void displayPhase1Table() {
		for (int i = 0; i < n; i++) {
			IntVar v = agent[i];
			System.out.print(i + 1 + ": ");
			DisposableValueIterator iterator = v.getValueIterator(false);
			int j;
			while (iterator.hasNext()) {
				j = iterator.next();
				System.out.print(pref[i][j] + 1 + " ");
			}
			System.out.println();
		}
	}

	void display() {
		System.out.println(n);
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n; j++)
				if (pref[i][j] != i)
					System.out.print((pref[i][j] + 1) + " ");
			System.out.println();
		}
	}

	void stats() {
		// System.out.println("cost:" + cost.getValue());
		System.out.print("solutions: " + solutions + " ");
		if (search)
			System.out.print("nodes: " + solver.getNodeCount() + "  ");
		System.out.print("modelTime: " + modelTime + "  ");
		if (search)
			System.out.print("solveTime: " + solveTime + "  ");
		System.out.print("totalTime: " + totalTime + "  ");
		System.out.print("modelSize: " + modelSize + "  ");
		System.out.print("readTime: " + readTime + " ");
		System.out.print("matchingSize: " + matchingSize + " ");
		// System.out.print("cost: "+ cost.getValue());
		System.out.println();
	}

	public static void main(String[] args) throws IOException, ContradictionException {
		SR sr = new SR(args[0]);
		sr.build("egal");
		if (args.length > 1)
			sr.solve(args[1]);
		else
			sr.solve("first");
		sr.stats();
	}
}
