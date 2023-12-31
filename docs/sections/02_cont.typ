#import "../template.typ": *
#import "@preview/lovelace:0.1.0": *

#show: setup-lovelace.with(line-number-supplement: "Zeile")
#let pseudocode = pseudocode.with(indentation-guide-stroke: .5pt)


== Continuous Case

#theorem[
  The Probability of sorting a list of $n$ numbers uniformly distributed between 0 and 1 using optimal strategy for maximizing the probability of getting the array sorted is: 


  
  $ P_n = integral_(0)^(1) sum_(k=1)^(n)  P_(n k) d n_1  $
  
  $ P_(n k)(n_1) = cases(
    0 "if" (P_(n k)(n_1) < P_(n (k_2!=k))(n_1)) and k in.not {0,n}, 
    "Bin"(n-1, k-1, n_1) P_(n-1-k) P_(k)  "else"
  ) $  

  Where $ P_(n k)(n_1)$ is the OSR of an $n$ elements array array if we starting with $n_1$ at the position $k$. And $"Bin"$ is the binomial distribution, with a success probability $P[n_2<n_1] = n_1 = p $ as $n in (0,1]$
  $ "Bin"(n, k, p) = binom(n, k) p^(n-k) p^(k)  $
]

#proof[
  Having the Optimal Sucess Rate (OSR) for $n<m$ slots, the OSR of $m$ slots is the expected value of optimally placing $n_1$ for each possible $n_1$.
  
  Placing the first number $n_1$ at the $k$ slot, divides the problem in two subdomains of itself with domains $[0,k-1]$ and $[k+1,1]$. Where the probability of having all the subsequent numbers correctly fitting in the new domains is given by a binomial distribution with $n-1$ trials, $k-1$ needed sucesses and a probability of succes $p = n_1$ .
]


The solution of the problem relies in the naive solution of $P_1=1$ for calculating the OSR for $n>1$ with the recursive formula which implements a "divide and conquer" strategy.



#figure(
  image("../figures/InfinitesimalSort_osr_20.png", width: 80%),
  caption: [Optimal Success Rate for $n$ slots, as seen in the figure, the probabilities of sorting it at once decrease in a exponential fashion.],
) <optimal_osr>


The OSR can always be found as an analytical solution, as all of the terms can be expressed in terms of polinomios and operations to polinomios.


In practice, for computing the OSR we can alternatively write the function by spliting the integral by the optimal ranges and defining $p_(n k) (n_1)$ as the probability of sorting the array given that we place the first element at the position $k$, so the solution will be given by the next formula:

$ P_n = sum_(k=1)^n integral_(O_(n k))^(O_(n k+1)) p_(n k) d n_1 $

With:
  $ p_(n k) (n_1) = "Bin"(n-1, k-1, n_1) P_(n-1-k) P_(k) $


$ O_(n k) = cases(
  0 "if" k =1, 
  "where" p_(n k)(n_1) = p_(n (k+1))(n_1),
  1 "if" k =n) 
$

We can see the representation of this solution in the @example_n_7, for the case $n=7$.

#figure(
  grid(
  columns: (1fr, 1fr),
  gutter: -30pt,
    image("../figures/InfinitesimalSort_domains_7.png", width: 80%),
    image("../figures/InfinitesimalSort_domains_in_range_7.png", width: 80%)
  ),
  caption: [Optimal Success Rate for $n$ slots, as seen in the figure, the probabilities of sorting it at once decrease in a exponential fashion.],
) <example_n_7> 



== The Sorting algorithm

Once we know the OSR discussed in the previous section, we can create a probabilistic algorithm for sorting an array in a online, non-adaptive way.

Given $n_1$ we only need to place it where  $p_(n k) (n_1)$ is maximun and for the next $n_m$ we have two posibilities:

  - $n_m$: can be placed in the new array, without breaking the order, then we normalize the n_m using the extremes where it fits: $t_m = (n_m-min)/(max-min)$ 
  - $n_m$: can not be placed in the new array. In this case the algorithm has failed in sorting but we can still get the best possible sort by ignoring the placed values and use the same algorithm with the empty slots.




Given the number of slots $n$ and the first number to place $n_1$ we place it by the index given by the optimal threshold $k$. Given $n_2$ we run the same algorithm but in the range $(k,n] forall n_2 > n_1$ or  $[0,k) forall n_2 < n_1$ normalizing $n_2$ as $t_2 = (n_2-min)/(max-min)$, where max and min are the biggest and smallest number we can fit in the subproblem.

For the next turns, there is the posibility that the index suggested by the threshold is already taken, in that case we will move the number in the direction that preserves the order as far as we need, but when there is no possible fit we have different posibilities that will further define the algorithm:

  - Ignore all items already in place and run the algorithm for the empty slots.
  - Try to place it in the neighbourhoud of the index that it corresponds, using some heuristics:
    - For instance we could go to the right or left till we find a place and if no place is found then switch the direction.
    - We could alternate left and right directions in an increasing pattern 1,-2,+3,-4 etc.
    - We could check wich option of the left or right placing let's the whole array in a more skewed postion, measuring center of mass for instance.

The problem of the heuristical approaches is that they don't consider the impact in the later game.



For $n_2$ if $n_2$ is bigger than $n_1$ we run the same algorithm but in the intre 


#algorithm(
  caption: [Pseudo Sort],
  pseudocode(
    <line:blinken>,
    [Create empty slots array],
    [get $n_1$],
    [Place it at $k=I(n_1)$, slots[k]=n_1 ],
    [get $n_2$ and $k_2=I(n_2)$],
    [*PROCEDURE* ],
    [*IF* $"slots"[k_2]$ is empty *then*], ind,
      [$"slots"[k_2] = n_2$ ], ded,
    [*ELIF $n_2 < "slots"[k_2]$ *],
    [],
    [Blinker aus],
  )
)

== prove of algorithm bestnes

What we in principle know about our algorithm is that it has the OSR, so the probabilities of sorting the array are maximized.

As the algorithm is recursive, this property is also satisfied at every subset of the array, and in case of failure to sort, as we choose to ignore placed items and apply the same algorithm, this property still applies.

But other properties remain still unclear in principle, specially for the case the algorithm it fails to do a perfect sort.

  + Are there algorithms that on average have higher Correctly Placed Items? (ACPI)
  + Are there algorithms that on average take more Turns till Failure (ATF)
  + Are there algorithms that results on average in a higher center of mass (ACM)
  + Are there algorithms that results on average in a smaller distance to correct position (AD)
  + Are there algorithms that results on average in a smaller average max distance to correct position (AMD)? 
  + Are there algorithms that on failure case sort better, in terms of center of mass etc? 


ACPI, We know that for $n=2$ the answer is trivially no, When we are in the position of having failed and rerun the algorithm in the subset we do

For the rest of the points let us explore the case of $n=2$ in that case is trivial to prove that the algorithm porpoused maximices CM and ICP at the time it minimices AD and AMD as it maximizes the probability of the two numbers being sorted.

For the case $n=3$ We need to think again in terms of the possibilities:

we can prove by contradiction most of the properties, imagine that there is an algorithm that in case of failure does have ha better ACPI, ATF, ACM or AD, that would mean that that algorithm would also be be
