package upmc.ri.bin;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import upmc.ri.index.*;
import upmc.ri.struct.STrainingSample;

/**
 * Created by gozuslayer on 11/11/16.
 */
public class VisualIndexes {
    public static void main(String[] args) {
        List<List<Integer>> res = new ArrayList<List<Integer>>();
        BufferedReader buff = new BufferedReader(new FileReader(filename));

        String line;
        // 1st line : describing file format
        line = buff.readLine();

        while ( (line = buff.readLine()) != null) {
            // skipping Image ID
            // words
            line = buff.readLine();
            String[] linesplit  = line.split(";",1100);
            List<Integer> wordsim = new ArrayList<Integer> ();

            for(int k=0;k<linesplit.length-1;k++){
                int word = 0;
                if(k==0)
                    word = Integer.parseInt(linesplit[k].substring(1,linesplit[k].length()));
                else
                    word = Integer.parseInt(linesplit[k]);
                wordsim.add(word);
            }
            // 3 lines for sikipping x-y-BB
            line = buff.readLine();
            line = buff.readLine();
            line = buff.readLine();
            res.add(wordsim);

        }

        buff.close();

        return res;


        String chaine="";
        String fichier ="/home/gozuslayer/DAC/DAC/RI/TP7/sbow/acoustic_guitar.txt";
        List<double[]> Bows;
        File f = new File("/home/gozuslayer/DAC/DAC/RI/TP7/RI_2016/upmc/ri/bin/acoustic_guitar.txt");
        int i = 1;
        try {
            BufferedReader in = new BufferedReader(new FileReader(f));
            String str = in.readLine();
            int k = 0 ;
            while ( (str !=null ) && k<10 )
            {
                String ID;
                int[] Bof ;
                double[] X ;
                double[] Y ;
                if (k==0)
                {
                    k=k+1;
                }
                else {
                    /*ID*/
                    if (k%5 == 1)
                    {
                        ID = str;
                    }

                    /*BOF*/
                    else if (k%5 == 2)
                    {
                        String[] BofString = str.substring(1, str.length() - 1).split(";");
                        for (String num : BofString)
                        {
                            Bof.add(Integer.parseInt(num));
                        }

                    }

                    /*X*/
                    else if(k%5 == 3)
                    {
                        String[] XString = str.substring(1, str.length() - 1).split(";");
                        for (String num : XString)
                        {
                            X.add(Double.parseDouble(num));
                        }
                    }

                    /*Y*/
                    else if (k%5 == 4)
                    {
                        String[] YString = str.substring(1, str.length() - 1).split(";");
                        for (String num : YString)
                        {
                            Y.add(Double.parseDouble(num));
                        }
                    }

                    /*BoundingBox*/
                    else if (k%5 == 0)
                    {
                        ImageFeatures ib = new ImageFeatures(X,Y,Bof,ID);
                        VIndexFactory vIndexFactory = new VIndexFactory();
                        double[] BoW = vIndexFactory.computeBow(ib);
                        STrainingSample<X,Y> image = new STrainingSample(BoW,i);


                    }


                    System.out.println(str);
                    k = k + 1;
                    str = in.readLine();
                }
            }
            in.close();
        } catch (IOException e) {
        }


    }

}
