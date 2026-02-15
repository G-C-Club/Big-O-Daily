[🇮🇷 Persian Version](./README-fa.md)

# Question: Seats
[**🔗 Problem Link**](https://codeforces.com/problemset/problem/2188/B)

### ⚙️ Details
| Feature | Specification |
| :--- | :--- |
| **👨‍💻 Author** | **Javad Abdolahi** [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/) [![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=flat&logo=telegram&logoColor=white)](https://t.me/javadabdolahi) |
| **📊 Score** | 1000 |
| **⏱️ Time Limit** | 1 second |
| **💾 Memory Limit** | 256 megabytes |
| **Tags** | `greedy` |

---
### 📖 Description
Cordell manages a row of $n$ seats at the *Scuola Comunale di Musica Piova* where students are strictly forbidden from sitting next to each other.

You are given a binary string$^{\text{∗}}$ $s$, where $s_i = \mathtt{1}$ indicates that the $i$-th seat has been occupied by a student, and $s_i = \mathtt{0}$ indicates that it is free now. It is guaranteed that no two adjacent seats are occupied currently. Cordell needs to add more students until it is impossible to seat anyone else in the row. However, she wants to achieve this state with as few students as possible.

Your task is to calculate the minimum **total** number of students seated when it is impossible to seat anyone else in the row.

$^{\text{∗}}$A binary string is a string where each character is either $\mathtt{0}$ or $\mathtt{1}$.

### 📥 Input Specification
Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le  t \le  10^4$). The description of the test cases follows.

The first line of each test case contains a single integer $n$ ($1 \le  n \le  2 \cdot 10^5$) — the number of seats in the row.

The second line of each test case contains the binary string $s$ of length $n$ ($s_i \in \{\mathtt{0}, \mathtt{1}\}$). It is guaranteed that no two adjacent characters are both $\mathtt{1}$.

It is guaranteed that the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$.

### 📤 Output Specification
For each test case, output a single integer — the minimum total number of seated students.

---
### 🧪 Samples
#### Sample 1
| Input | Output |
| :--- | :--- |
| <pre>5<br>1<br>0<br>3<br>000<br>5<br>00000<br>6<br>100101<br>13<br>0000100001000</pre> | <pre>1<br>1<br>2<br>3<br>5</pre> |

### 📝 Note
In the first test case, $n = 1$ and the hall is initially empty. Because the row is still possible to seat any student, Cordell must place one student at seat $1$. Therefore, the minimum number of seated students is $1$.

In the third test case, Cordell can place two students at seats $1$ and $4$. It can be shown that she cannot place only one student so that the row is impossible to seat anyone more, so the answer is $2$.

In the fourth test case, no extra students can be seated, so Cordell can place no extra students, and the number of seated students is $3$.


---
*Note: These problem statements have been automatically retrieved by the bot.*