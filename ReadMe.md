# Wordle formally

The wordle rules look simple. But it is tricky to formalize them.

- If the guess (from now on $g$) and the word ($w$) coincide in position $i$ ($g[i]=w[i]$), the feedback is correct ($f[i]={\color{green}\text{CORRECT}}$).
- If the characters at position $i$ do not match but $g[i]$ occurs in $w$ at position $j$, the result is present (or wrong position) $f[i]={\color{orange}\text{PRESENT}}$.
  But only if no other character got its result from $w[j]$.
  We will formalize this aspect using a marked array $m$ with backreference to $g$.
- Otherwise the result is wrong ($f[i]={\color{black}\text{WRONG}}$).

The formal specification of the feedback is split into parts for better readability.
In every formula, we quantify over the position $i$. The idea is to describe for a position $i$ what the feedback is. Due to symmetry, every position is handled the same.
We use integer theories in the formulas but everything could be lowered to first-order logic in a straight-forward way (or CP/SMT solvers can be used).

For every part, we will give the formula and a reading in natural language.

$f[i]={\color{green}\text{CORRECT}} \lor f[i]={\color{orange}\text{PRESENT}} \lor f[i]={\color{black}\text{WRONG}}$

The feedback for every character in the guess is either correct, present, or wrong.

$f[i]={\color{green}\text{CORRECT}} \leftrightarrow g[i]=w[i]$

A character is correct iff. guess and word coincide.

$\forall j.~m[j]=i \to w[j]=g[i] \land (f[i]={\color{green}\text{CORRECT}} \lor f[i]={\color{orange}\text{PRESENT}})$

Only characters that correspond to the one in guess are marked in the word $w$.
We create a mark for a character exactly when it is correct or present (but not for wrong).

$\mathrm{someMarked} := \exists j.~m[j]=i$

A formula to express that there is a mark for the cell $g[i]$.
(The let is implemented using auxiliary variables and equalvalence constraints)

$f[i]={\color{green}\text{CORRECT}} \lor f[i]={\color{orange}\text{PRESENT}} \to \mathrm{someMarked}$

A correct cell or present cell has to be marked by specification of marked.

$\forall j.~j\neq i \to m[i]\neq m[j]$

There can not be two marks for the same cell.

$m[i]<|g|$

The marks are negative (for unmarked) or point to a cell in $g$.

$g[i]\neq w[i] \land \mathrm{someMarked} \to f[i]={\color{orange}\text{PRESENT}}$

A marked character in $g$ that is not the same as the corresponding one in $w$ has to be present.

$\mathrm{noSmallerUnmarked} := \lnot \exists i_2.~ i_2 \lt i \land g[i]=g[i_2] \land \lnot \exists l.~m[l]=i_2$

There is no previous (smaller position) in $g$ with the same character that is unmarked.

$f[i]={\color{orange}\text{PRESENT}} \to \mathrm{someMarked} \land \mathrm{noSmallerUnmarked}$

Recall: For multiple possible cells that can be present, the cells are assigned present from left to right. If there are three 'E' in $g$ which are not correct and there are two 'E' in $w$, the first two 
'E' from $g$ are assigned present.
A present cell has to be marked and no previous cell of same content can be unmarked.

$f[i]={\color{black}\text{WRONG}} \to \forall j.~w[j]=g[i]\to m[j]\geq 0\land m[j]\neq i$

A wrong char either has no correspondence in $w$ ($\lnot (\exists j.~ g[i] = w[j])$ which is already included in the second part) or is a failed present.
That is, every corresponding character is marked.

$\lnot (\exists j.~ g[i] = w[j]) \to f[i]={\color{black}\text{WRONG}} \land \lnot \mathrm{someMarked}$

If there is not corresponding character in $w$, the character in $g$ is assigned wrong.


## Whole Formula

The whole formula is:

$$
\forall g~w.~\exists f~m.~\forall i.~ \\
(f[i]={\color{green}\text{CORRECT}} \lor f[i]={\color{orange}\text{PRESENT}} \lor f[i]={\color{black}\text{WRONG}}) \land \\
(f[i]={\color{green}\text{CORRECT}} \leftrightarrow g[i]=w[i]) \land \\
(\forall j.~m[j]=i \to w[j]=g[i] \land (f[i]={\color{green}\text{CORRECT}} \lor f[i]={\color{orange}\text{PRESENT}})) \land \\
  \forall \mathrm{someMarked}.~ (\mathrm{someMarked} \leftrightarrow \exists j.~m[j]=i) \to \\
(f[i]={\color{green}\text{CORRECT}} \lor f[i]={\color{orange}\text{PRESENT}} \to \mathrm{someMarked}) \land \\
(\forall j.~j\neq i \to m[i]\neq m[j]) \land \\
m[i]<|g| \land \\
(g[i]\neq w[i] \land \mathrm{someMarked} \to f[i]={\color{orange}\text{PRESENT}}) \land \\
  \forall \mathrm{noSmallerUnmarked}.~ (\mathrm{noSmallerUnmarked} \leftrightarrow \lnot \exists i_2.~ i_2\lt i \land g[i]=g[i_2] \land \lnot \exists l.~m[l]=i_2) \to \\
(f[i]={\color{orange}\text{PRESENT}} \to \mathrm{someMarked} \land \mathrm{noSmallerUnmarked}) \land \\
(f[i]={\color{black}\text{WRONG}} \to \forall j.~w[j]=g[i]\to m[j]\geq 0\land m[j]\neq i) \land \\
(\lnot (\exists j.~ g[i] = w[j]) \to f[i]={\color{black}\text{WRONG}} \land \lnot \mathrm{someMarked})

$$
