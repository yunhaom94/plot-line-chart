# plot-line-chart

Basically we are expecting a csv that pass in series that needs to be plotted.

In put csv is sample.csv that follows a few rules
```
1. Data comes in pairs, one col of x, one col of y
2. Data can be in any length
3, Padding from shorter series must be ,, aka NaN
4. Y col name (i.e. series 1) will be legend name
5. Three entries followed by the y col are styles, linestyle, marker and color
6. Different styles of defining style is shown in sample.csv
7. Leading and trailing space is removed

A few prints using the sample.csv, change xlim ylim if needed
     x  series 1    x   series 2   x.1  series 3
0  1.0         4  1.1          3   1.2         5
1  2.0         4  2.1          4   2.2         7
2  3.0         5  3.1          6   3.2         9
3  4.0         8  4.1          4   4.2         4
4  NaN        --  5.1          5   NaN    dotted
5  NaN         o  NaN          -   NaN         4
6  NaN       red  NaN          x   NaN      blue
7  NaN       NaN  NaN  #11aa0055   NaN       NaN
X:
[1.0, 2.0, 3.0, 4.0]
Y:
[4.0, 4.0, 5.0, 8.0]
Style:
['--', 'o', 'red']
X:
[1.1, 2.1, 3.1, 4.1, 5.1]
Y:
[3.0, 4.0, 6.0, 4.0, 5.0]
Style:
['-', 'x', '#11aa0055']
X:
[1.2, 2.2, 3.2, 4.2]
Y:
[5.0, 7.0, 9.0, 4.0]
Style:
['dotted', '4', 'blue']
```

# plot-grouped-bar-chart

Basically we are expecting a csv with trailing optional style
Note that all series shares the same x as x is not numeric

```
Rules:
1. Attribute so far is just color for bar charts
2. Hardcoded group width is 1, so more series, each one will get thinner
3. Expect all series as values
4. If X dim == Y dim then no style, otherwise last entry is style
5. Trailing x space for color setting mus tbe NaN which is ,, in csv

Sample:

  x_str  series 1  series 2  series 3
0    Q1         4       1.1         3
1    Q2         4       2.1         4
2    Q3         5       3.1         6
3    Q4         8       4.1         4
4   NaN       red      blue     green
0.25
X:
['Q1', 'Q2', 'Q3', 'Q4']
Y:
[4.0, 4.0, 5.0, 8.0]
Style:
['red']
X:
['Q1', 'Q2', 'Q3', 'Q4']
Y:
[1.1, 2.1, 3.1, 4.1]
Style:
['blue']
X:
['Q1', 'Q2', 'Q3', 'Q4']
Y:
[3.0, 4.0, 6.0, 4.0]
Style:
['green']

```