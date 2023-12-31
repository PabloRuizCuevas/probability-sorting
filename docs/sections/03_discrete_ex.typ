#import "../template.typ": *

== One Bucket

The trivial case:

$ P_(1, m) = 1 $

== Case two buckets 

For $n=2$ there are two possible strategies for placing $n_1$:

$ L: {1}{0} \ R: {0}{1} $ 

Let's consider the case $m=6$:

$ "list" = [1,2,3,4,5,6] $

#figure(
    table(
      columns: (1fr, 1fr, 1fr, 1fr),
      inset: 3pt,
      align: horizon,
      [$n_1$], "Strategy", [*formula*], [*probability*],
      "1", "S1", $ (m-k)/(m-1) $, $5/5 $,
      "2", "S1", $ (m-k)/(m-1) $, $4/5 $,
      "3", "S1", $ (m-k)/(m-1) $, $3/5 $,
      "4", "S2", $ (k-1)/(m-1) $, $3/5 $,
      "5", "S2", $ (k-1)/(m-1) $, $4/5 $,
      "6", "S2", $ (k-1)/(m-1) $, $5/5 $,
    ),
    caption: ""
  ) <table>

With an average of $4/5$ we get theformula:

$ P_(2,m ) = 1/m (sum_(k=1)^(floor(m/2))(m -k)/(m -1 ) +  sum_(k= floor(m/2)+1)^(m) (k-1)/(m -1 )) $


== Three buckets case

Let's consider the case $m=10$:

$ "list" = [1,2,3,4,5, 6,7,8,9,10] $

$ L: {1}{0}{0} \ C: {0}{1}{0} \ R: {0}{0}{1} $ 



#figure(
    table(
      columns: (1fr, 1fr, 2fr, 1fr),
      inset: 3pt,
      align: horizon,
      [$n_1$], "Strategy", [*formula*], [*probability*],
      "1", "S1", $ P_(2,m-1) $, $ 1 $,
      "2", "S1", $ H(10,8,2, 2) P_0 P_(2,m-2) $, $0.62 P_(2, m-2) $,
      "3", "S1", $ H(10,7,2, 2) P_0 P_(2,m-3) $, $ 0.46 P_(2, m-3) $,
      "3", "S2", $ H(10,7,2, 1) P_1 P_1 $, $ 0.46  $,
    ),
    caption: ""
  ) <table>

We see that 3 is already better to have strategy 3 , the H coeficicient is the same, but:
$ P_1> P_(2,m-1) $


Fnally we obtain the formula:

$ P_(3,m ) = 1/m (
  &sum_(n_1=1)^O_(3,1) H(m,m-n_1,2, 2) P_0 P_(2,m-n_1) +  \
  &sum_(O_(3,1)+1)^(O_(3,2)) H(m,m-n_1,2, 1) P_1 P_1 +  \
  &sum_(O_(3,2) +1)^(m) H(m,m-n_1,2, 0) P_(2,n_1-1) P_0 ) 
$

That can be written as:

$ P_(3,m ) = 1/m  sum_(k=1)^3 
sum_(n_1=O_(3k))^(O_(k+1)) H(m,m-n_1,2,  3-k) 
P_(k-1,n_1-1)  
P_(3-k,m-n_1) $

