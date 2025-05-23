
## Moderando el conflicto interno de opiniones en una red social (ModCI)

### Anotaciones:

Una red social $RS$ es una pareja $< SAG, R_{max} >$, donde:

- $SAG = <sa_o,...sa_{n-1}>:$ Secuencia de grupo de agentes.

	- $sa_i = <n_i^{RS},o_{i,1}^{RS},o_{i,2}^{RS},r_i^{RS}>:$ Grupo de agentes. donde:
		- $n_i^{RS}:$ Numero de agentes que pertenecen al grupo de agentes $i$.
		- $o_{i,1}^{RS}:$ Opinión de los agentes del grupo de agentes $i$ de la red $RS$ sobre la afirmación 1. Va de -100 (en desacuerdo) a 100 (de acuerdo).
		- $o_{i,2}^{RS}:$ Opinión de los agentes del grupo de agentes $i$ de la red $RS$ sobre la afirmación 2. Va de -100 (en desacuerdo) a 100 (de acuerdo).
		- $r_i^{RS}:$ Rigidez de los agentes del grupo de agentes $i$ de la red $RS$ para $0\leq i<n$.

- $R_{max}:$ Valor entero máximo que se cuenta para moderar las opiniones de $RS$. $R_{max} \geq 0$ 


El  valor del conflicto interno de una red $RS$ se puede definir de la siguiente forma:

$$
CI(RS)= \frac{\sum_{i=0}^{n-1}(n_{i}^{RS}*(o_{i,1}^{RS}-o_{i,2}^{RS})^2)}{n}
$$


Anteriormente tenía esta fórmula:

$$
CI(RS)= \frac{\sum_{i=0}^{n-1}(n_{i}^{RS}*(o_{i,1}^{RS}-o_{i,2}^{RS})^2)}{\sum_{i=0}^{n-1}n_{i}^{RS}}
$$

Sin embargo de decidió cambiarla por temas de facilidad.

Una estrategia de cambio de opinión de una red $RS$ (de ahora en adelante lo llamaremos $E$) se define como: 

$$
< e_{0},e_{1},\dots,e_{n-1} > | \text{ } e_{i} \in \{ 0,1,2,\dots,n_{i}^{RS} \}
$$

donde $e_{i}$ representa el número de agentes del grupo de agentes $i$ a los cuales se le ha cambiado su opinión por medio de $E$.

Aplicar esta estrategia da como resultado una nueva red $RS'$ con la misma estructura que la red $RS$ pero donde la opinión de los agentes cuya opinión ha sido cambiada ahora tiene el mismo valor en $o_{i,1}^{RS'}$ y $o_{i,2}^{RS'}$. Es decir, si $ModCI(RS,E)=RS'$ entonces:

$$
  n_{i}^{RS'}= 
  \begin{cases}
    n_{i}^{RS}-e_{i} & \text{si $e_{i} > 0$} \\
    n_{i}^{RS} & \text{si $e_{i}=0$}
  \end{cases}
$$

Se asume que los agentes a los cuales ajustó su opinión por medio de $E$ ya no hacen parte de $RS'$.

El valor de esfuerzo de ajustar las opiniones sobre $RS$ con la estrategia $E$ se define de la forma:

$$
Esfuerzo(RS,E)=\sum_{i=0}^{n-1} \lceil |o_{i,1}^{RS}-o_{i,2}^{RS}|*r_{i}^{RS}*e_{i} \rceil 
$$

Hay que tener en cuenta que $Esfuerzo(RS,E)\leq R_{max}$ 


## Aplicación con Programación Dinámica

Sea $M[i,r]$ una matriz de tamaño $i\times (r + 1)$:

$$
M[i,r]=
\begin{cases}
0 & \text{si  $i=0$ $\land$ $r=0$ } \\ \\
\min\limits_{\substack{0\leq e\leq n_{i}}} \{ M[i-1,r-esfuerzo(i,e)] + conflicto(i,e)\}  & \text{si $esfuerzo(i,e)\leq r$}  \\ \\
\infty & \text{en otro caso}
\end{cases}
$$

Donde $esfuerzo(i,e)$ representa el esfuerzo individual del grupo $i$. $conflicto(i,e)$ representa el conflicto individual del grupo $i$.

## Requisitos

- Python 3.8 o superior  
- pip

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/paelsam/modelamiento-conflicto-interno.git
cd modelamiento-conflicto-interno
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:

```bash
python main.py
```

## IMPORTANTE (usuarios Windows)

En el archivo `main.py`, si estás en Windows, debes **descomentar** la siguiente línea y **comentar** la que está debajo:

```python
self.state("zoomed")  # Para usuarios de Windows
# self.attributes('-zoomed', True)
```