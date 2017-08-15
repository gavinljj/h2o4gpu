import time
import sys
import os
import numpy as np
import logging
import feather

print(sys.path)

try:
    from utils import find_file, runglm, elastic_net
except:
    from tests.utils import find_file, runglm, elastic_net

logging.basicConfig(level=logging.DEBUG)


def fun(nGPUs=1, nFolds=1, nLambdas=100, nAlphas=8, validFraction=0.2, verbose=0,family="elasticnet", print_all_errors=False):
    t = time.time()

    print("cwd: %s" % (os.getcwd()))
    sys.stdout.flush()

    print("Reading Data")
    df = feather.read_dataframe("./tests/data/bnp.feather")
    print(df.shape)
    X = np.array(df.iloc[:, :df.shape[1] - 1], dtype='float32', order='C')
    y = np.array(df.iloc[:, df.shape[1] - 109], dtype='float32', order='C')
    print("Y")
    print(y)

    t1 = time.time()
    logloss_train, logloss_test = elastic_net(X, y, nGPUs=nGPUs, nlambda=nLambdas, nfolds=nFolds, nalpha=nAlphas,
                                        validFraction=validFraction, verbose=verbose,family=family,print_all_errors=print_all_errors)

    # check logloss
    print(logloss_train[0, 0])
    print(logloss_train[0, 1])
    print(logloss_train[0, 2])
    print(logloss_test[0, 2])
    sys.stdout.flush()

    #Always checking the first 3 alphas with specific logloss scores (.48,.44)
    if validFraction==0.0 and nFolds > 0:
        assert logloss_train[0, 0] < .14
        assert logloss_train[0, 1] < .14
        assert logloss_train[1, 0] < .003
        assert logloss_train[1, 1] < .003
        assert logloss_train[2, 0] < .001
        assert logloss_train[2, 1] < .001
    if validFraction > 0.0:
        assert logloss_train[0, 0] < .008
        assert logloss_train[0, 1] < .008
        assert logloss_train[0, 2] < .008
        assert logloss_train[1, 0] < .006
        assert logloss_train[1, 1] < .006
        assert logloss_train[1, 2] < .007
        assert logloss_train[2, 0] < .0004
        assert logloss_train[2, 1] < .0004
        assert logloss_train[2, 2] < .0004

    print('/n Total execution time:%d' % (time.time() - t1))

    print("TEST PASSED")
    sys.stdout.flush()

    print("Time taken: {}".format(time.time() - t))

    print("DONE.")
    sys.stdout.flush()


def test_glm_bnp_gpu_fold5_quick_train(): fun(nGPUs=1, nFolds=5, nLambdas=5, nAlphas=3, validFraction=0.0,verbose=0,family="logistic",print_all_errors=False)
def test_glm_bnp_gpu_fold5_quick_valid(): fun(nGPUs=1, nFolds=5, nLambdas=5, nAlphas=3, validFraction=0.2,verbose=0,family="logistic",print_all_errors=False)


if __name__ == '__main__':
    test_glm_bnp_gpu_fold5_quick_train()
    test_glm_bnp_gpu_fold5_quick_valid()