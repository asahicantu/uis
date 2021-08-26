# STA500 Probability and Statistics course
In this repository all contents, problems and work related to this course will be posted here


## Markov
### Transitions
* Commuticative ->
* Accessible ->
  Absorbing [No exit]
  Recurrent R_i = 1 (Guarranteed to return)
  Transient (Not guarranteed to return)
  Finite MC has at least one recurrent state
  If one state in a class is recurrent, all states  in the class are (Recurrent Class)
  If one state in a class is transient, all states in the class are (Transient class)
  In an irreducible Markov chain all states are either recurrent or  transient
  In a finite irreducible Markov chain, all states are recurrent

  For a Markov chain with finite state space, all recurrent states are positive recurrent.
  Once a Markov chain enters a recurrent class, it will remain in that class forever

  Pweiod: Greatest Common Divisor between transitions
  Aperiodic : Period 1 p_ii > 0
  All states in a class have the same period

  Steady state probabilities:
  * Irreducible
  * Positive recurrent
  * Aperiodic

If the state space is finite: Irreducible + finite state space ⇒ positive recurrent, i.e. [only need to check Irreducible and Ap]


Positive recurrent: The expected number of transitions between two visits to the state is finite

Null recurrent: The expected number of transitions between two visits to the state is infinite

#### 
Irreducible: Only 1 class
Not Irreducible => More than 1 class