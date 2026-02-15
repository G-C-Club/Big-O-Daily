[🇮🇷 Persian Version](./README-fa.md)

# Question: Game with a Fraction
[**🔗 Problem Link**](https://codeforces.com/problemset/problem/2196/A)

### ⚙️ Details
| Feature | Specification |
| :--- | :--- |
| **👨‍💻 Author** | **Javad Abdolahi** [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/) [![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat&logo=telegram&logoColor=white)](https://t.me/javadabdolahi) |
| **📊 Score** | Unknown |
| **⏱️ Time Limit** | 2 seconds |
| **💾 Memory Limit** | 256 megabytes |
| **Tags** | `games`, `math` |

---
### 📖 Description
Alice and Bob have two integers $p$ and $q$, and they are playing a game with these numbers. The players take turns, with Alice going first. On their turn, a player can do one of two actions:

- decrease $p$ by one (this action is possible if $p  \gt  0$);
- decrease $q$ by one (this action is possible if $q  \gt  1$).
The game ends when $p = 0$ and $q = 1$.

Bob wins if at any point during the game the fraction $\frac{p}{q}$ is equal to **in value** the fraction $\frac{2}{3}$. Otherwise, Alice wins.

Given the initial values of $p$ and $q$, determine the winner of the game if both players play optimally.

### 📥 Input Specification
Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le  t \le  10^4$). The description of the test cases follows.

Each input case consists of a single line containing two integers $p$ and $q$ ($1 \le  p, q \le  10^{18}$).

### 📤 Output Specification
For each input case, output:

- " `Alice` " if Alice wins;
- " `Bob` " if Bob wins.

---
### 🧪 Samples
#### Sample 1
| Input | Output |
| :--- | :--- |
| <pre>6<br>4 6<br>10 14<br>15 15<br>7 12<br>7000000000000000 10487275715782582<br>1000000000000000000 1000000000000000000</pre> | <pre>Bob<br>Bob<br>Alice<br>Alice<br>Bob<br>Alice</pre> |

### 📝 Note
In the first input case, the fraction is already equal to $\frac{2}{3}$ by value, so Bob wins.

In the second input case, one possible sequence of the game is as follows:

- initially $p = 10, q = 14$;
- after Alice's turn $p = 9, q = 14$;
- after Bob's turn $p = 9, q = 13$;
- after Alice's turn $p = 9, q = 12$;
- after Bob's turn $p = 8, q = 12$.
Bob wins, as $\frac{8}{12}$ is equal to $\frac{2}{3}$. It can be shown that in this example, with optimal play from both players, Bob always wins.

For the third input case, Alice's optimal strategy will be to decrease $q$ as long as possible. In this case, the game will end in favor of Alice regardless of Bob's actions.


---
*Note: These problem statements have been automatically retrieved by the bot.*