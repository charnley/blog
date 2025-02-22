---
layout: post
title:  "Compiling and setting up GAMESS"
date:   2012-08-31
categories: chemistry gamess
---

> **_NOTE 2025 Feb:_** Disclaimer, this guide is very old and most likely setting up GAMESS is way easier.

Small guide on how to setup the QM software [GAMESS](http://www.msg.ameslab.gov/gamess/) on a normal Ubuntu computer and work in parallel with multiple nodes (via sockets).
Loosely this is based on [this guide](http://molecularmodelingbasics.blogspot.dk/2010/08/compiling-gamess-on-linux-pc.html) on how to compile GAMESS.

## Setup

I'm going to pretend that you are working on Ubuntu 12.04 LTS, but I'm sure you can relate it to whatever distribution you are working on.
Download and compile

1. Download the newest GAMESS from [http://www.msg.ameslab.gov/gamess/License_Agreement.html](http://www.msg.ameslab.gov/gamess/License_Agreement.html)

2. Run config

in the shell

    ./config

and answer the questions. Answer them truthfully.

3. Compile DDI

DDI is used to run the GAMESS executable, compile it by

    make ddi

4. Compile GAMESS

After compiling DDI and setting up the config, we can just write

    make

and everything will happen automatically. You can add the flag "-j4" if you
have 4 CPU's and want the compiling to go a little faster. It takes a few
minutes.

## Compiling without Math library

Note on compiling without a math library, like MKL. In some versions of GAMESS the linking will fail with error message like "including missing subroutines for vector operations failed". This is what the math libraries are used for. For Ubuntu you can install  BLAS and LAPACK easily with

    sudo apt-get install libblas3gf libblas-doc libblas-dev
    sudo apt-get install liblapack3gf liblapack-doc liblapack-dev

Now we just need to change the ``./liked`` script and add some compiler flags. 
If you are compiling with gfortran then you need to find and update the following two lines in ./lked under the gfortran section.

    - set BLAS='blas.o'
    - set MATHLIBS=' '
    + set BLAS=''
    + set MATHLIBS='-lblas -llapack '

and similar if you are using ifort to compile edit the section in lked and set the correct compiler flags.
and then it should liked alright.

## Update rungms

To run GAMESS there is a included a run script in the root folder, which needs to be updated located in the beginning, for the scratch folder and GAMESS path. so, edit (using VIM, if you are awesome, EMACS, if you are not).

    vi rungms

and set following paths to the correct (and obviously not my username);

    set SCR=/home/$USER/scr
    set USERSCR=/home/$USER/scr
    set GMSPATH=/home/$USER/opt/gamess

Note: GAMESS doesn't work?!

Pro tip by +Anders Christensen
If this is the first time you are trying to get GAMESS working on your Linux machine, you will need to set kernel.shmmax to 1610612736. This is done by either;

    /sbin/sysctl -w kernel.shmmax=1610612736

or if you don't want to do the command (or don't have root access) every time you boot up, open the file called:

    /etc/sysctl.conf

and add the following line:

    kernel.shmmax=1610612736

Running the GAMESS testcase (exam)
Included in GAMESS is a list of input files to be tested to see if the software
is working as it should. This is also useful to run if you do changes to the
source code. Go to the root of the GAMESS folder and write.


    ./runall
    ./tests/standard/checktst

This will then output all the exams. If all is passed, then GAMESS should be working alright.


## Setting up cluster calculation

If you want to have GAMESS working with a cluster system then there are a few things to change.
This is to get the parallelization with sockets to work.

### 1. Update rungms

You'll need to edit the part of rungms that checks the hostname of the current node. As present the rungms check if you are running calculations on any of the Iowa nodes (where GAMESS is developed), and you are probably not.

Find the following if-statement and switch;


    if ($NCPUS > 1) then
        switch (`hostname`)


and locate the default switch case, and outcomment the "exit", just because the rungms doesn't regonize your hostname. If you are using a cluster system, you are probably using some kind of queuing system, like PBS og LoadLeveler. Here is what you need to change on the specific system;

### 1.1 PBS specific

PBS should be working out-of-the box. As long as you have fixed the above hostname exit. If you don't need the user-scratch file, you can set $USERSCR to "/scratch/$PBS_JOBID" as $SCR, under


    if ($SCHED == PBS) then


### 1.2 LoadLeveler specific

As default, rungms does not contain loadleveler default settings, so you will need to setup the following test.


    if ($?LOADL_STEP_ID) set SCHED=LOADL

under 'batch schedular' section, and then add the case

    if ($SCHED == LOADL) then
        set SCR=/scratch/$LOADL_STEP_ID
    endif


If you don't use the $USERSCR output, you can set that too the local scratch folder as well.

### 2. Setting up input file

If you are running the calculation across multiple nodes, you'll need to tell the GAMESS executable how many nodes you are using, this is done simply by stating, fx. for 10 nodes;


     $gddi
      ngroup=10
     $end

     $system
      mwords=256
     $end

in the input file, with mwords being how much memory you want to allocate.

Remember: Remember that you need 1 space before the sections on GAMESS input files.

## The end

And that's it. So simple and easy out-of-the-box. You should be running loads of QM calculations now.

Happy GAMESS'ing

## Comments

The original blogpost is very old, and moved from blogspot. It got some critique which will be included here


> Always select "sockets" and never "MPI"!

*Unknown 17 February 2014 at 09:21*

> Actually, PBS does _not_ work out of the box because the defaults are some obscure and based on a computer cluster at ISU in Ames.
>
> You should change
> 
> if (`uname` == Linux) set NETEXT=".myri"
> 
> into
> 
> if (`uname` == Linux) set NETEXT=""
> 
> because you do most likely not have a myrinet network and similarly you should set the line
> 
> set spacer2=":netext="
> 
> to
> 
> set spacer2=""
> 
> That will make it run on PBS.

*Unknown 17 February 2014 at 10:44*

> Actually, there is more:
> 
> 1) For an FMO calculation, the ridiculous amount of memory you have specified (5000 mega words = 40 GB) is a serious waste. Use something more like 256 (which is 2 GB) or even half of that. This memory will be allocated per core depending on your setup and the type of calculation you are running.
> 
> 2) if you are not going to make something other than having 10 groups (10 nodes) then it is a waste to actually have the NGRFMO(1)=10 specified. NGRFMO is used to control the number of groups specified for each part of a calculation and if you do not specify anything, then NGRFMO(1)=NGROUP.
> 
> 3) in general it is a bad idea to set USERSCRtoSCR when you are running on a cluster. There might be files you are interested in which will be lost when the queue-system cleans up after you.

*Unknown17 February 2014 at 10:50*
