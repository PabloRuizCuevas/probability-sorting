#import "../template.typ": *

= Integers with no Replacement

In this case the numbers are uniformly distributed between 1 and $m$ with no repetition.

For this case, the solution will be very similar as the continius one, but taking into account that the distributions will be hypergeometrical ones as there is no replacement.


$ H("population_size","succesfull population", "trials", "sucesses needed")  $



== Case n Buckets

Generalizing the last formula we can obtain the general case:

$ P_(n,m) = 1/m  sum_(k=1)^n
sum_(n_1=O_(n,k))^(O_(n,k+1)) H(m,m-n_1, n-1, n-k) 
P_(k-1,n_1-1)  
P_(n-k,m-n_1) $

Where:


$ P_(n_k,m) (n_1) =  H(m,m-n_1, n-1, n-k) 
  P_(k-1,n_1-1)  
  P_(n-k,m-n_1)
$

$ O_(n,k) := cases( 
  0 "if" k = 1, 
  m "if" k = n, 
  max{n_1 in ZZ | P_(n_k,m)(n_1) >  P_(n_(k+1),m) (n_1)}
) $ 


The last part can also be expresed as:

$ O_(n, k ) = floor(n_1) "where" 0<P_(n_k,m)(n_1) =  P_(n_(k+1),m) (n_1) $

Using this definition, we can rewrite the solution as:

$ P_(n,m) = 1/m  sum_(k=1)^n sum_(n_1=O_(n,k))^(O_(n,k+1))  P_(n_k,m)(n_1)  $

the bracket thing may make no sense.

/*
def Hypergeometric(name, N, m, n):
    r"""
    Create a Finite Random Variable representing a hypergeometric distribution.

    Parameters
    ==========

    N : Positive Integer
      Represents finite population of size N.
    m : Positive Integer
      Represents number of trials with required feature.
    n : Positive Integer
      Represents numbers of draws.
*/

#theorem[
  The square of any real number is non-negative.
]

#proof[
  Any real number $x$ satisfies $x > 0$, $x = 0$, or $x < 0$. If $x = 0$,
  then $x^2 = 0 >= 0$. If $x > 0$ then as a positive time a positive is
  positive we have $x^2 = x x > 0$. If $x < 0$ then $−x > 0$ and so by
  what we have just done $x^2 = (−x)^2 > 0$. So in all cases $x^2 ≥ 0$.
]



#pagebreak()

