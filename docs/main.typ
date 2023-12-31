#import "template.typ": *


#show: ams-article.with(
  title: "Strategic Online Placement: An Algorithm for Real-time, Distribution-Informed Positioning",
  authors: (
    (
      name: "Pablo Ruiz Cuevas",
      department: [Department of my room],
      organization: [My self],
      location: [Munich,  80636],
      email: "pablo.r.c@live.com",
      url: "www.math.sc.edu/~howard"
    ),
  ),
  abstract: "In numerous systems, from manufacturing to aviation and from data management to emergency response, the challenge arises to position or sort incoming items in real-time based on their inherent characteristics and without the luxury of rearrangement. This paper introduces the Strategic Online Placement Algorithm (SOPA), a novel approach that leverages prior distribution knowledge to make optimal placement decisions as items arrive. Unlike traditional sorting algorithms, SOPA is designed for scenarios where items, once placed, cannot be moved. We demonstrate the broad applicability of SOPA across various domains and show that, with accurate distribution information, our method is the optimal placement strategy for the given information.",
  bibliography-file: "refs.bib",
)


#include{"sections/01_intro.typ"}
#pagebreak()
#include{"sections/02_cont.typ"}
#pagebreak()
// #include{"sections/02_cont_ex.typ"}
#pagebreak()

// #include{"sections/03_discrete.typ"}
// #include{"sections/03_discrete_ex.typ"}