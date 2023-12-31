#import "../template.typ": *

= Introduction


In numerous systems spanning manufacturing, aviation, data management, and emergency response, there emerges a unique challenge: how to optimally position or sort incoming items in real-time, based on their inherent characteristics, and without the ability to reposition them later. Traditional sorting algorithms, which operate by comparing and potentially swapping elements, may not be suitable or efficient for these scenarios. This paper introduces the Strategic Online Placement Algorithm (SOPA), a novel approach that leverages prior distribution knowledge to make optimal placement decisions as items arrive, ensuring efficient system operations and improved outcomes.


== Related Work:

Online sorting and placement algorithms have a rich history, with many algorithms designed for specific scenarios such as stream processing, memory management, and real-time systems. Traditional online algorithms, like the ones proposed by Kushwaha et al. (2021), focus on adaptively sorting data but often rely on the possibility of rearranging items. Other works, such as those by [Author of the Mapping Sorting Algorithm paper et al., Year], have touched upon non-adaptive sorting but without the incorporation of prior distribution knowledge. A notable advancement in this domain is the work of Chaikhan et al. (2022) who proposed a fast continuous streaming sort algorithm for big streaming data environments under fixed-size single storage. This algorithm particularly addresses the constraint of storage overflow in real-time systems, which resonates with the problem scenario of fixed placement discussed in this paper. However, the existing literature including the work of Chaikhan et al. (2022) does not delve into leveraging prior distribution knowledge for optimal item placement, which is the focal point of this paper. Clearly, a gap exists for an approach that combines real-time placement, non-adaptiveness, and distribution-aware decision-making.

#pagebreak()

== Problem Definition:

Given a stream of N items arriving sequentially, the objective is to place each item in a fixed position within an array of length N based on its characteristics. Two primary constraints define this problem:

- Online Processing: Items are processed in the order they arrive, without knowledge of future items.
- Non-adaptive Placement: Once an item is placed in a position, it cannot be moved.

The placement decisions should leverage known or estimated distributions of the items' characteristics to achieve optimal or near-optimal sorting. The "optimality" in this context can be defined based on specific goals, such as minimizing disruptions in a sequence, ensuring balanced weight distribution, or any other domain-specific objective.

We will solve the problem for the case where:

- Continuous case where $N ∼ U(0,1)$
- Discrete case without replacment where $N∼U{1,2,...,M}$

This cases can be extended without loss of generalitly to any other distribution, as we will proof.

In this paper we will show the best posible algorithm/strategy to maximize the probability of sorting the array, as well as the probability of succesfully sorting the array using the optimal algorithm. We will refer to this probability as the *Optimal Success Rate* (OSR)


