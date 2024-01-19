# fourier-transforms

Visualization gui for fourier transformations

Heavily inspired by a 3 Blue 1 Brown [video](https://www.youtube.com/watch?v=spUNpyF58BY) on the topic. It's well worth a watch!

A visualization to for sinusoid wave forms and fourier transforms.
The gui is made up of 6 six interacive plots. The first three plots allow
you to create sinusoid waves with varying frequency, phase shift, and amplitude.
The next plot allows you to visualize adding the three sinusoids together.

The last two plots help to visualize the fourier transform, going from the
time domain to the frequency domain. The first plot here allows you to visualize
the math behind the fourier tranform by wrapping
the sinusoid around a circle at a given, varying, frequency and plotting the *mean* of the signal.
The last plot is the output of the **fourier transform itself, also mapping
the mean point from the previous plot over to show the correlation.

## Installation and Dependencies

This project depends on `numpy`, `matplotlib` and `ttkbootstrap`.
Install from `pyproject.toml`, `poetry.lock`, or directly with `pip`:

`pip install numpy`
`pip install matplotlib`
`pip install ttkbootstrap`

## Running

To run the gui, simply run the `main.py` file:

`python3 main.py`

I hope you enjoy!
