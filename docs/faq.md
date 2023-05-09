# Frequently asked Questions

## How can I debug my experiment?

To debug your experiment, you need to add a run configuration to your favorite IDE.
Here is an example on [how to do this in PyCharm](#how-can-i-add-a-run-configuration-to-pycharm).

Some parts of the training need an additional configuration, to make them debuggable. E.g. Debugging metrics,
the loss or net callbacks. To debug them, you need to set the `RUN_EAGERLY` parameter of your .env file to `True`

## How do I use my own run configuration for a niceML pipeline?

**niceML** runs its pipelines via [dagster](https://dagster.io/).
If you want to start the pipelines in the terminal, just use the following code snippet,
replace the path and run it in your terminal. 

``` ssh
dagster job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/<path to your job yaml>
```

## How can I add a run configuration to PyCharm?

If you want to use your own pipeline configuration or are tired to type the make commands into the terminal,
PyCharm offers you to use run configurations.

In PyCharm, search for the run configuration editor. Usually it can be found in the upper right corner of PyCharm.
Otherwise, search the
[official PyCharm documentation](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html) to find it.

Add a new configuration using the Python template. Switch the 'target' from 'script path' to 'module name', and
set it to use 'dagster'. The 'Parameters' are what you would type in the terminal after the module name.
In case of a training, you can adjust the following code to your needs and add it to the configuration:

``` ssh
job execute -m niceml.dagster.jobs.repository -j job_train -c configs/jobs/<path to your job yaml>
```

If needed, you can make the '.env' file available for your trainings run. Just add your .env-file and
check 'Enable EnvFile' in the 'EnvFile' tab of the run configuration.

Save everything, and you are ready to run and debug your experiment.

> **Tipp:** You can also add a run configuration for the dashboard. Just set the module name to `streamlit
> and the parameters to `run niceml/dashboard/dashboard.py configs/dashboard/<path to your dashboard yaml>`

## With which use-cases can **niceML** help me?

## Can I use PyTorch with **niceML**?

Currently, no. But we want to implement it in future versions of **niceML**.
