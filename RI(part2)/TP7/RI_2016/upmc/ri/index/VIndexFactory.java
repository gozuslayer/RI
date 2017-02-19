package upmc.ri.index;
import java.util.List;
/**
 * Created by gozuslayer on 11/11/16.
 */
public class VIndexFactory {

    public static double [] computeBow(ImageFeatures ib){
        List <Integer> words = ib.getwords();

        double[] result = new double[ib.tdico];

        for (Integer item : words){
            result[item]++;
        }

        /*Calcul somme totale du nombre de mots dans image*/
        double sumresult = 0;
        for (int i=0; i<result.length;i++){
            sumresult += result[i];
        }

        /*Normalisation*/
        for (int k=0 ; k<result.length ; k++){
            result[k] = result[k]/sumresult;
        }
        return result;

    }
}

