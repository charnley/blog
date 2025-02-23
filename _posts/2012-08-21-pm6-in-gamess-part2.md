---
layout: post
title:  "PM6 in GAMESS, Part 2"
date:   2012-08-31
categories: chemistry gamess
---

Okay, so I'm still working on implementing PM6 integrals in GAMESS.

I got the source code from MOPAC 7.1 which includes d-integrals for the MNDO-D method (which is what Jimmy Stewart is using for PM6 in the newest MOPAC (hopefully), which originates from a program written by Walter Thiel).

So the strategy is simply to 'export' the subroutines / modules from MOPAC 7.1 needed to replicate the d-integrals in GAMESS (written in Fortran 90),  and 'import' them into GAMESS-US.
Now, the semi-emperical part of GAMESS-US is actually based on a older version of MOPAC (written in Fortran 77) so the subroutines should be very similar to the code I'll be trying to import.

First part of this mission is too map the relevant subroutines in both GAMESS and MOPAC. And hopefully I'll be able too se a pattern and merge the 'trees'.

The map for MOPAC is:

![Subroutine map for MNDO MOPAC]({{ site.baseurl }}/assets/images/pm6_mndod_submap.png)
*Figure 1: Subroutine map of MNDO in MOPAC*

And the map for GAMESS is:

![Subroutine map for MNDO GAMESS]({{ site.baseurl }}/assets/images/pm6_gamess_submap.png)
*Figure 2: Subroutine map of MNDO in MOPAC*

Now I just need an idea for merging the two trees. Since Stewart based his d-integrals on code he got from Thiel it seems like most of the subroutines is collected in a single file called mndod.F90 (fitting name, lol).

This means I 'just' (I beginning to hate that work) need to copy-and-paste the file into GAMESS and make sure the file is hooked to GAMESS common blocks instead of the fortran 90 modules from MOPAC. So step 1: Include the file and make it compile (which is a lot of rewriting interfaces and modules into the actual file so it is a standalone solution.)

The highlighted area is only the first part of the problem though. After the fock matrix has been put together with the new and cool d-items the matrix needs to be solved and we need the fockd1 and fockd2 for that. They are conveniently also put in the same file with the rest of the subroutines.

Furthermore I have been told by +Jan Jensen that I need to watch out for 'guessmo' subroutine when implementing the new integrals. As described in his figure;

![Subroutine map for GAMESS]({{ site.baseurl }}/assets/images/pm6_janhjensen_subroutine_map.jpg)
*Figure 3: Subroutine map of MNDO in MOPAC*

So to recap, implementation in 5 easy steps (said in a very television kitchen accent):

Step 1: Get mndod.f90 compiled with gamess (using gamess common blocks instead of mopac modules and interfaces)

Step 2: Integration: Make IF(PM6) and run the mndod code instead of gamess with pm6 parameters and more.

Step 3: Integration: Make IF(PM6) and run the fock-d 1 and 2 instead in mpcg()

Step 4: Find out why it does not work and solve the problem.

Step 5: Celebration.

To be continued!
