$$
\bold{B}(t)=(1-t)^3\bold{P_0}+3t(1-t)^2\bold{P_1}+3t^2(1-t)\bold{P_2}+t^3\bold{P_3}, t\in[0,1]
$$

Per component:
$$
B_x(t)=(1-t)^3P_{0,x}+3t(1-t)^2P_{1,x}+3t^2(1-t)P_{2,x}+t^3P_{3,x}\\
B_y(t)=(1-t)^3P_{0,y}+3t(1-t)^2P_{1,y}+3t^2(1-t)P_{2,y}+t^3P_{3,y}
$$
By definition $\bold{B}$ intersects the points $(0,0)$ and $(1,1)$ . Hence, $(0,0) \in \bold{B}$  and $(1,1)\in \bold{B}$ . If we let $\bold{B}$ run from $(0,0)$ for $t=0$ to $(1,1)$ for $t=1$ , it follows:
$$
B_x(0)=P_{0,x}=0\\
B_y(0)=P_{0,y}=0\\
B_x(1)=P_{3,x}=1\\
B_y(1)=P_{3,y}=1
$$
Now, $\bold{B}$ simplifies to:
$$
B_x(t)=3t(1-t)^2P_{1,x}+3t^2(1-t)P_{2,x}+t^3\\
B_y(t)=3t(1-t)^2P_{1,y}+3t^2(1-t)P_{2,y}+t^3
$$
Because we want to be able to find the roots (numerically, using `numpy`), we will rewrite it to a standard cubic polynomial:
$$
\begin{split}
B_x(t) & =3t(1-2t+t^2)P_{1,x} + (3t^2 - 3t^3)P_{2,x} + t^3 \\
& = (3t - 6t^2 + 3t^3 )P_{1,x} + (3t^2 - 3t^3)P_{2,x} + t^3 \\
& =(3P_{1,x}-3P_{2,x}+1)t^3 +(-6P_{1,x}+3P_{2,x})t^2 +3P_{1,x}t \\
\end{split}
$$

$$
\begin{split}
B_y(t) & =3t(1-2t+t^2)P_{1,y} + (3t^2 - 3t^3)P_{2,y} + t^3 \\
& = (3t - 6t^2 + 3t^3 )P_{1,y} + (3t^2 - 3t^3)P_{2,y} + t^3 \\
& =(3P_{1,y}-3P_{2,y}+1)t^3 +(-6P_{1,y}+3P_{2,y})t^2 +3P_{1,y}t \\
\end{split}
$$

With $\bold{P}=\bold{P_0}$ and $\bold{Q}=\bold{P_1}$:
$$
B_x(t) =(3p_x-3q_x+1)t^3 +(-6p_x+3q_x)t^2 +3p_xt\\
B_y(t) =(3p_y-3q_y+1)t^3 +(-6p_y+3q_y)t^2 +3p_yt
$$

$$

$$

