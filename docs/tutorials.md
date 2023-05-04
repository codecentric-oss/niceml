# Tutorials

This part of the project documentation focuses on a
**learning-oriented** approach. You'll learn how to
get started with the code in this project.

## Getting started

This is a short tutorial to get you started with **niceML**.
You will 

- generate a test dataset,
- train your first Semantic Segmentation Model and
- take a look at the results using the **niceML** dashboard.

### 0. Installation

> **Note:** If you already installed **niceML** and tested your installation, you can head on to Step 3.

After cloning the **niceML** repository to your computer, you can use the Makefile as an entry point.
At frist you should install all needed packages for training and the dashboard.
Use the

```ssh
make install
```

command in your console or, if you want to use the Apple Silicon GPU, type in

```ssh
make install_macos
```

To test, whether your installation works, run

```ssh
make pytest
```

and check that all tests ran successfully.

### 1. Generate test data

**niceML** provides a test dataset of images with random numbers at random positions on them.
To generate the dataset, run:

```ssh
make generate_data
```

### 2. Train a Semantic Segmentation

There are a few already configured pipelines you can use to train your model.
To start a test training using semantic segmentation, run:

```ssh
make train_semseg
```

### 3. Start the dashboard

The dashboard helps you to evaluate your trainings results. To start the dashboard locally, run:

```ssh
make dashboard
```

On the dashboard you can get an overview of your trainings. 
E.g. how many epochs the model was trained, what image size was used,
how different metrics performed during the training.
You can also have a look at the image data and configurations used.
If you want to use the dashboard for remote trainings in the future,
you are also able to download certain training files.

Perform another Semantic Segmentation or one of the other experiment types.
You can get an overview of the currently available trainings types by looking at
the Makefile or the following codeblock, which is basically copied from the Makefile:

```ssh
make train_semseg # Semantic Segmentation
make train_objdet # Object Detection
make train_regression # Regression
make train_classification_multitarget # Multitarget Classification
make train_classification_binary # Binary Classification
make train_classification_softmax # Classification using Softmax
```

After you ran a few trainings, you can make yourself familiar with the different dashboard components.
In the future you may write your own dashboard components, which can be easily implemented.
If you are interested, take a look at this tutorial: [How to implement a new dashboard component](how-to-guides.md)
