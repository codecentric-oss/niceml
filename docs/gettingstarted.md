# Getting started



## Installation

After cloning the niceML repository to your computer, you can use the Makefile as an entry point:

```ssh
make install
```

of if you want to use the Apple Silicon GPU

```ssh
make install_macos
```

To test, whether your installation works, run:

```ssh
make pytest
```

## Generate test data

niceML provides a test dataset of images with random numbers at random positions on them. To generate the dataset, run:

```ssh
make generate_data
```

## Train a Semantic Segmentation

With niceML you can run a variety of trainings. To start a test training using semantic segmentation, run:

```ssh
make train_semseg
```

## Start the dashboard

The dashboard helps you to evaluate your trainings. To start the dashboard locally, run:

```ssh
make dashboard
```

You may alter the dashboard in `configs/dasboard.local.yaml`.
