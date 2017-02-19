package upmc.ri.struct.training;

import upmc.ri.struct.Evaluator;
import upmc.ri.struct.STrainingSample;
import upmc.ri.struct.instantiation.IStructInstantiation;
import upmc.ri.struct.model.IStructModel;

import java.util.List;
import java.util.Random;

/**
 * Created by gozuslayer on 24/11/16.
 */
public class SGDTrainer<X,Y> implements ITrainer<X,Y>{
    public Evaluator<X,Y>;

    public static double[] train(List<STrainingSample<X, Y>> lts , IStructModel<X,Y> model){
       double[] weights = new double[lts.size()];
        double pas = 0.1;
        double lambda=1;
        int iteration = 1000;

       for (int i=0;i<iteration;i++)
       {
            for (int j = 0;j<lts.size();j++)
            {
                Random randomizer = new Random();
                STrainingSample<X,Y> randomX_Y = lts.get(randomizer.nextInt(lts.size()));
                Y yhat = model.lai(randomX_Y);
                STrainingSample<X,Y> randomX_Yhat = new STrainingSample<X, Y>(X,yhat);
                double[] gi = model.instantiation(randomX_Yhat).psi(X,yhat) - model.instantiation(randomX_Y).psi(randomX_Y.input,randomX_Y.output);

                for (int k = 0;i<gi.length;i++)
                {
                    weights[k] = weights[k]-pas*(weights[k]*lambda+gi[k]);
                }
            }
       }
        return weights;
    }

    public static convex_loss(List<STrainingSample<X,Y>> lts, IStructModel<X,Y> model){
        double right;
        for (int i = 0; i < lts.size(); i++) {
            for (int j = 0 : i<lts.size();i++){

            }
        }
    }
}
