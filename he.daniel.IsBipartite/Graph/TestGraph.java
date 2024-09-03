import java.util.*;

import java.io.*;

public class TestGraph {

	static final String fileName = "GraphVertices.txt";
	
	public static void main(String[] args) throws FileNotFoundException{
		System.out.print("Enter the name of the input file");
		Scanner in = new Scanner(System.in);
		String fileName = in.nextLine();
		
		
		File file = new File(fileName);
		Scanner reader = new Scanner(file);
		
		//load number of vertices
		int vertices = Integer.parseInt(reader.nextLine());
		
		//load edges
		int[][] edges = new int[vertices][vertices];
		for (int v = 0; v < vertices; v++) {
			String line = reader.nextLine();
			//separate into whitespace, splitting by whitespace
			String[] data = line.split("\\s+");
			
			//first value on each line is supposed to be the origin of the edge
			int origin = Integer.parseInt(data[0]);
			
			//run through all but the first value (since it was supposed to be the origin value)
			for (int i = 1; i < data.length; i++) {
				int value = Integer.parseInt(data[i]);
				edges[origin][value] = 1;
			}
		}
		
		reader.close();
		
		//generate graph
		UnweightedGraph<Integer> graph = new UnweightedGraph<Integer>(edges, vertices);
			System.out.println("\nPart 1");

			/*
			 * Connected graph detection algorithm:
			 * 	Run DFS from any vertex.
			 * 	The graph is connected iff all vertices have been visited.
			 */
			AbstractGraph.Tree dfsTree = graph.dfs(0);
			if (dfsTree.getNumberOfVerticesFound() != graph.getSize()){
				System.out.println("Not connected.");
			}
			else{
				System.out.println("Connected.");
				HashSet hs = new HashSet();
				boolean flag = false;
				for (Object x : dfsTree.getSearchOrder()){
					int c = 0;
					for (Integer blah: graph.getNeighbors((int) x)){
						if (hs.contains(blah)){
							c += 1;
						}
					}
					if (c > 1){
						flag = true;
						break;
					}					
					hs.add(x);
				}
				if (flag){
					System.out.println("Cyclic.");
				}
				else{
					System.out.println("No Cycles.");
				}
			}			
	}
}
