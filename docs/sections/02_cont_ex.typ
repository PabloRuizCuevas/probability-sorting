#import "../template.typ": *
#show: setup-lovelace

== Start:

In this paper we will calculate the probability of sorting an array at once, when the numbers follow a uniform distribution with no repetition:

$ P[x] ~ U(0,1) $

With a probability density function of:

$ f (x) =  cases( 1 "if" x in [0,1], 0 "else" ) $

We well create an algorithm to optimally solve this problem, given that the numbers cannot be moved once they are on place.

== Solution:

Considering no repetition, and N elements in the array, having N bukets.

Analizing simple cases trivial case:

$ P_(1) = 1 $



As there is only one bucket and one number we can always place  a random number:

=== Two buckets


$ P_(2) =  3/4 = 0.75 $

To calculate $P_(2)$ let's consider without loss of generality that we get a first  number $n_1$ the probability of $n_2$ being bigger than $n_1$ is:

$ P[n_2 > n_1] = 1 - n_1 = 1 - p_1 $

and:
$ P[n_2 < n_1] = n_1 = p_1 $

If we naively place in the second bucket, the probability of success would be:

$ P_(k 1 n ) = p_1 $

With $p_1 $ following a uniform distribution the expected value will be:

$ E[x] = integral_(-infinity)^infinity p f(x) dot d p=   integral_(-infinity)^infinity p U(0,1) dot d p = integral_(0)^1 p dot d p = 1/2 $


But for an optimal strategy, we can place the number in the first or the second bucket depending on his value, with a trivial thershold at $n=1/2$, if $n>1/2$ will be placed in the sencond bucket otherwise in the first, with this consideration we get a new expected value of:

$ P_(2) = cases(P[n_2 > n_1] "if" 0 < n_1 <= 0.5,
                  P[n_1 > n_2] "if" 0.5 < n_1 < 1) $

$ P_(2) = cases(1-n_1 "if" 0 < n_1 <= 0.5,
n_1 "if" 0.5 < n_1 < 1) $

Taking $n_1$ as $p$ then:

$ P_(2) & = integral_(0)^(1/2) (1-p) dot d p + integral_(1/2)^(1) p dot d p \ &= lr(p - (p²) / 2  |)_(0)^(1/2) + lr((p²) / 2  |)_(1/2)^1 \ & = (1/2 - 1/8) + (1/2 - 1/8) \= 3/4  $

Notice the symmetry of the probabilties and that the $p=1/2$ can be justified by the inequality:

$ (1-p) < p =>  0.5  < p $

Which imposes using the second strategy i.e. placing the first number in the bucket 2 if $p_1 > 0.5$ (or if n_1 > 0.5).


=== Three buckets

For three buckets we have different posibilities. 

$ L: {1}{0}{0} $ 
$ C: {0}{1}{0} $ 
$ R: {0}{0}{1} $ 

So the Probability would be:


$ P_(3) = cases(
  (1 - n_1)^2  P_(2) "if" 0 < n_1 <= n_("opt1"),
  2n_1 (1-n_1)  "if" 0.5 < n_1 < 1, 
  n_1 P_(2)^2 "if" 0 < n_1 <= n_("opt2")
) $


