#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <chrono>
#include <cassert>

using namespace std;

const int M = 999; // just based on the concrete game at placeitgame.app
const int N = 30;  // just based on the concrete game at placeitgame.app

vector<double> logFactorial(M + 1);
vector<vector<double>> opt(M + 1, vector<double>(N + 1, 0));

// Function to compute the logarithm of the binomial coefficient; used to avoid overflows.
double logBinomialCoefficient(int n, int k)
{
    if (k == 0 || k == n)
        return 0.0;
    return logFactorial[n] - logFactorial[k] - logFactorial[n - k];
}

// Function to compute the hypergeometric probability
double hypergeometricProbability(int N, int K, int n, int k)
{
    if (N - K < n - k || K < k) {
        return 0.0;
    }

    double logP = logBinomialCoefficient(K, k) +
                  logBinomialCoefficient(N - K, n - k) -
                  logBinomialCoefficient(N, n);
    return std::exp(logP);
}


int main()
{

    auto start = chrono::high_resolution_clock::now();

     // compute log-factorials
    for (int i = 0; i < M+1; ++i) {
        if (i <= 1) {
            logFactorial[i] = 0.0;
        } else {
            logFactorial[i] = logFactorial[i - 1] + std::log(i);
        }
    }

    for (int m = 0; m <= M; m++) {
        for (int n = 0; n <= N; n++) {
            if (n <= 1) {
                opt[m][n] = 1.0;
                continue;
            }
            double sum = 0.0;
            int best_j = 1;
            for (int i = 1; i <= m; i++) {
                double mx = 0.0;
                double prev = 0.0;
                for (int j = best_j; j <= n; j++) {
                    double p = opt[i - 1][j - 1] * opt[m - i][n - j] * hypergeometricProbability(m-1, i-1, n-1, j-1);
                    if (p < prev) {
                        break;
                    }
                    if (p >= mx) {
                        mx = p;
                        best_j = j;
                    }
                    prev = p;
                }
                sum += mx;
            }
            opt[m][n] = sum / m ;
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;
    cout << "Time taken: " << duration.count() << " seconds" << endl;

    int m = 999, n = 20;
    cout << "OPT(" << m << ", " << n << ") = " << opt[m][n] << endl;
    
    return 0;
}
