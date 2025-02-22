---
layout: post
title:  "Calculate RMSD from two XYZ files "
date:   2013-04-26
categories: chemistry
---

I want to calculate the RMSD (Root-mean-square deviation) between two molecule structures in XYZ format. And after googling around I concluded that the easiest way to do it was to use pymol. However being a CLI user, I do not want to download the files and open up a GUI all the time, I just want a script that can do it via a terminal. Time for a little google and python project.

Calculating the RMSD mathematically for two sets of xyz coordinates for n particles is straight forward:

$$
\mathrm{RMSD}(v,w) = \sqrt{  \frac{1}{n} \sum_{i=1}^n ((v_{ix} - w_{ix})^2 + (v_{iy} - w_{iy})^2 + (v_{iz} - w_{iz})^2 ) }
$$

However this is without taking into account that the two molecules could be identical and only translated in space.
To solve this we need to position the molecules in the same center and rotate one onto the other.

The problem is solved by first find the centroid for both molecules and translating both molecules to the center of the coordinate system.
Then we need an algorithm to align the molecules by rotation. For this I found [Kabsch algorithm](http://dx.doi.org/10.1107%2FS0567739476001873) from 1976.

> It is a method for calculating the optimal rotation matrix, that minimzes the RMSD between two paired set of points
> 
> http://en.wikipedia.org/wiki/Kabsch_algorithm

The algorithm is nicely written out on wikipedia, so it was straight forward to implement (still took me a little time though). So I wont go into details of it here.

However it is clear that the centering the molecules using their centeroid could possibly not be the best way of finding the minimal RMSD between two vector sets. So +Lars Bratholm got the idea of using a fitting function, fitting the center of the molecules and using Kabsch to calculate a minimal RMSD.

**Code:** You can find the code and examples here: github.com/charnley/rmsd

Usage:

    ./calculate_rmsd.py molecule1.xyz molecule2.xyz


**Results:** The output will then be "pure rmsd", "rmsd after rotation" and "rmsd after fit".

Note; for a testcase I calculated the rmsd for a molecule set with 140 atoms, to be ~0.15, and when I did the same calculation in pymol I got 0.092. However pymol did state that it was cutting 20 atoms, but didn't state which, where as my script takes all the atoms into account.
