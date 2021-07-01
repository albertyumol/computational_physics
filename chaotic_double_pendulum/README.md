# Objective

Analyze flip elapsed time of a double pendulum given the initial configuration.

The study of **double pendulums** isn't remotely developed, partly due to the fact there are **no exact solution** to the coupled differential equations, but also due to the randomness of the system. **Data visualization** of a measure of the **randomness** of the double pendulum, the measure being the flip elapsed time, may help organize and search for interesting initial conditions.

## Problem

1. For which initial conditions will the pendulum flip? Not flip?

2. Analyze the points for which the pendulum does not flip outside the energetically-forbidden region (EFR).

## Solution

**Primary procedures for solving problem:** Runge-Kutta Method, Numerical Intersection, Numerical Iteration, Graphing & Visualization

**Predicted outcomes:** fat fractal, unflip points outside EFR

## Methodology

1. Double pendulum equations of motion reduced to Hamiltonian’s equations for two angles and two momenta
2. Ruge-Kutta method used to solve for momenta and angles given initial conditions where both momenta are zero and both angles varying depending on desired dimensions.
3. Conditions involve both angles intersecting to either –π or π, where angles are measured positively CCW from –vertical axis of each c.s. with mass at the origin. Also, when <img src="https://render.githubusercontent.com/render/math?math=2\coscos \theta_1 %2B \cos \theta_2 ≥ 1">, t is 1010s, implying an energetically forbidden region for flipping.
