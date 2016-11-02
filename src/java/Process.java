package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org._dmis.object.BioEntityExtractorTree;
import org._dmis.object.BioEntityInfo;

public class Process {
	static BioEntityExtractorTree bet;
	
//	public static void process(File f) {
//		try {
//			BufferedReader br = new BufferedReader(new FileReader(f));
//			BufferedWriter bw = new BufferedWriter(new FileWriter(new File("outputs/pubmed_entity_found/" + f.getName())));
//			String l;
//
//			while((l=br.readLine())!=null){
//				HashSet<BioEntityInfo> hs = bet.extractEntities(l);
//				String writeLine = l;
//				for(BioEntityInfo e : hs){
//					if(e.getName().split(" ").length > 1){
//						String temp = e.getName().replace(" ", "_");
//						writeLine = writeLine.replace(e.getName(), temp);
//					}
//				}
//				bw.write(writeLine);
//				bw.newLine();
//			}
//			bw.close();
//			br.close();
//			
//		} catch (FileNotFoundException e) {
//			e.printStackTrace();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
//	}

	public static void main(String args[]) {
		
		String dictFilePath = "res/WordNetChecked_bossNewDic_2016-04-25.txt";
		String xrefFilePath = "res/xref_bossNewDic_2016-04-25.txt";
		bet = new BioEntityExtractorTree(dictFilePath);
		bet.loadXref(xrefFilePath);
		
//		String dir = "/home/sunkyu/workspace/PathwayMaker/res/pubmed_sentences/";
//		String dir = "/home/sunkyu/workspace/PathwayMaker/res/preprocessed_archive/";
		String dir = "/home/sunkyu/workspace/BioWord2Vec/res/ncbi wsd 2013/all/";
		File text_dir = new File(dir);
		File[] texts = text_dir.listFiles();
		
		int THREADCOUNT = 3;
		ExecutorService exec = Executors.newFixedThreadPool(THREADCOUNT);
		// 쓰레드풀 생성하고 전부다 사용후에는 반드시 셧다운 해야함~
		for(File f : texts){
			exec.execute(new ProcessThread(f, bet));
		}
		exec.shutdown();
	}
}

class ProcessThread implements Runnable{
	private File textFile;
	private BioEntityExtractorTree bet;
	public ProcessThread(File f, BioEntityExtractorTree bet){
		this.textFile = f;
		this.bet = bet;
	}
	@Override
	public void run() {
		try {
			BufferedReader br = new BufferedReader(new FileReader(textFile));
			BufferedWriter bw = new BufferedWriter(new FileWriter(new File("outputs/wsd2013/" + textFile.getName())));
			String l;

			while((l=br.readLine())!=null){
				HashSet<BioEntityInfo> hs = bet.extractEntities(l);
				String writeLine = l;
				for(BioEntityInfo e : hs){
					if(e.getName().split(" ").length > 1){
						String temp = e.getName().replace(" ", "_");
						writeLine = writeLine.replace(e.getName(), temp);
					}
				}
				bw.write(writeLine);
				bw.newLine();
			}
			bw.close();
			br.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}