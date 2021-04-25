from test_omp import *
# import pandas as pd

if __name__ == "__main__":
    # Repeat test a few times to get rid of random variation in system load
    times_to_repeat_tests = 10

    # Comment these out depending on what you want to run!
    ALGORITHMS_TO_RUN = [
        "sklearn",
        # "v0_original",
        "naive_omp"
    ]

     # = []
    # PROBLEM_SIZES = ["SMALL", "MEDIUM", "LARGE", "HUGE"]
    # for problem_size in PROBLEM_SIZES:
    #     print("-----Problem size: ", problem_size, " -----")
        #
        # if problem_size == "SMALL":
        #     n_components, n_features = 1024, 100
        #     n_nonzero_coefs = 17
        #     n_samples = 3000
        # elif problem_size == "MEDIUM":
        #     n_components, n_features = 1024, 100
        #     n_nonzero_coefs = 17
        #     n_samples = 3000
        # elif problem_size == "LARGE":
        #     n_components, n_features = 1024, 100
        #     n_nonzero_coefs = 17
        #     n_samples = 3000
        # elif problem_size == "HUGE":
        #     n_components, n_features = 1024, 100
        #     n_nonzero_coefs = 17
        #     n_samples = 3000

    y, X, w = make_sparse_coded_signal(
        n_samples=n_samples,
        n_components=n_components,
        n_features=n_features,
        n_nonzero_coefs=n_nonzero_coefs,
        random_state=0)

    avg_ylen = np.linalg.norm(y, 2, 0)

    # print("Settings used for the test: ")
    print("Number of Components: " + str(n_components))
    print("Number of Features: " + str(n_features))
    print("Number of Nonzero Coefficients: " + str(n_nonzero_coefs))
    print("Number of Samples: " + str(n_samples))
    print("\n")
    print("---Running each test ", times_to_repeat_tests, " times!---\n")


    # print('Single core. New implementation of algorithm v0 (pytorch)')
    # with torch.autograd.profiler.emit_nvtx():
    #     with elapsed_timer() as elapsed:
    #         xests_v0_new_torch = omp_v0_torch(torch.as_tensor(y.copy()), torch.as_tensor(X.copy()), n_nonzero_coefs)
    #     print('Samples per second:', n_samples/elapsed())
    #     print("\n")
    #
    # print('error in new code (blas)', np.max(np.abs(xests_v0_blas - xests_v0_new_torch.numpy())))

    # exit()

    # Optimized Naive implementation (not really Naive though?)
    if "naive_omp" in ALGORITHMS_TO_RUN:
        print('Single core. Optimized Naive implementation without Gramian/factorization tricks')
        results, errors = [], []
        for i in range(times_to_repeat_tests):
            with elapsed_timer() as elapsed:
                xests_naive = omp_naive(X.copy(), y.copy(), n_nonzero_coefs)
            # print('Samples per second:', n_samples/elapsed())
            results.append(n_samples/elapsed())
            err_naive = np.linalg.norm(y.T - (X @ xests_naive[:, :, None]).squeeze(-1), 2, 1)
            errors.append(err_naive)
        print("\n\n\n---Results for (", times_to_repeat_tests, " repeats)---")
        print("Mean: ", np.mean(results))
        print("Std: ", np.std(results))
        print("Average error: ", np.mean(errors))




    # print('Single core. Original V0 algorithm - Cholesky')
    # with elapsed_timer() as elapsed:
    #     xests_v0 = omp_v0_original(y.copy(), X.copy(), X.T @ X, (X.T @ y.T[:, :, None]).squeeze(-1), n_nonzero_coefs)
    # print('Samples per second:', n_samples/elapsed())
    # print("\n")
    # err_v0 = np.linalg.norm(y.T - (X @ xests_v0[:, :, None]).squeeze(-1), 2, 1)
    # print("Error: ", err_v0, '\n')
    #
    # print('Single core. Improved V0 algorithm - Cholesky + BLAS')
    # with elapsed_timer() as elapsed:
    #     xests_v0_blas = omp_v0_new_blas(y.copy(), X.copy(), X.T @ X, (X.T @ y.T[:, :, None]).squeeze(-1), n_nonzero_coefs)
    # print('Samples per second:', n_samples/elapsed())
    # print("\n")

    # exit()

    # precompute=True seems slower for single core. Dunno why.


    if "sklean" in ALGORITHMS_TO_RUN:
        omp_args = dict(n_nonzero_coefs=n_nonzero_coefs, precompute=False, fit_intercept=False)
        print('Single core. Sklearn')
        omp = OrthogonalMatchingPursuit(**omp_args)
        results_sklearn, error_sklearn = [], []
        for i in range(times_to_repeat_tests):
            with elapsed_timer() as elapsed:
                omp.fit(X, y)
            # print('Samples per second:', n_samples/elapsed())
            results_sklearn.append(n_samples/elapsed())
            err_sklearn = np.linalg.norm(y.T - (X @ omp.coef_[:, :, None]).squeeze(-1), 2, 1)
            error_sklearn.append(err_sklearn)
            # print("Avg. Error: ", np.average(err_sklearn / avg_ylen))
        print("---Results: Sklearn (", times_to_repeat_tests, " repeats)---")
        print("Mean: ", np.mean(results_sklearn))
        print("Std: ", np.std(results_sklearn))
        print("Average error: ", np.mean(error_sklearn))


    # err_naive = np.linalg.norm(y.T - (X @ xests_naive[:, :, None]).squeeze(-1), 2, 1)
    # err_v0 = np.linalg.norm(y.T - (X @ xests_v0[:, :, None]).squeeze(-1), 2, 1)
    # err_v0_new = np.linalg.norm(y.T - (X @ xests_v0_new[:, :, None]).squeeze(-1), 2, 1)
    # err_sklearn = np.linalg.norm(y.T - (X @ omp.coef_[:, :, None]).squeeze(-1), 2, 1)
    avg_ylen = np.linalg.norm(y, 2, 0)
    # print(np.median(naive_err) / avg_ylen, np.median(scipy_err) / avg_ylen)


    # ----PLOTTING FUNCTIONS------

    # plt.plot(np.sort(err_naive / avg_ylen), label='Naive')
    # plt.plot(np.sort(err_v0 / avg_ylen), '.', label='v0')
    # plt.plot(np.sort(err_v0_new / avg_ylen), '.', label='v0_new')
    # plt.plot(np.sort(err_sklearn / avg_ylen), '--', label='SKLearn')
    # plt.legend()
    # plt.title("Distribution of relative errors.")
    # plt.show()


    # exit(0)
    # # ---------MULTI CORE---------
    # no_workers = 2 # os.cpu_count()
    # # TODO: Gramian can be calculated once locally, and sent to each thread.
    # print('Multi core. With', no_workers, "workers on", os.cpu_count(), "(logical) cores.")
    # inputs = np.array_split(y, no_workers, axis=-1)
    # with multiprocessing.Pool(no_workers, initializer=init_threads, initargs=(solveomp, X, omp_args)) as p:  # num_workers=0
    #     with elapsed_timer() as elapsed:
    #         result = p.map(solveomp, inputs)
    # print('Samples per second:', n_samples / elapsed())

    # dataset = RandomSparseDataset(n_samples, n_components, n_features, n_nonzero_coefs)
    # sampler = torch.utils.data.sampler.BatchSampler(SequentialSampler(dataset), batch_size=2, drop_last=False)

    # y_est = (X @ omp.coef_[:, :, np.newaxis]).squeeze(-1)
    # residuals = np.linalg.norm(y.T - y_est, 2, 0)

    # plt.hist(residuals)
    # plt.show()

