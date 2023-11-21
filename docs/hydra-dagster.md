
## Hydra Configuration in combination with Dagster

Hydra is a powerful configuration system that makes it easy to write and manage configuration files for complex applications. Hydra uses a YAML file format to define configuration settings that can be used across different parts of an application. In this tutorial, we'll see how to use Hydra to configure niceML's machine learning pipeline with Dagster.

### Understanding Hydra Configurations

Hydra allows users to define a hierarchical set of configuration files that can be used to configure different parts of an application. The configuration hierarchy is defined in terms of "groups", which are essentially directories that contain YAML files. Each YAML file represents a configuration "scope" that can be used to define settings for different parts of an application.

Hydra also allows for "defaults", which are YAML files that contain commonly used settings that can be imported into other YAML files. This is particularly useful for niceML's machine learning pipelines, where certain settings are shared across different parts of the pipeline.

### Using Hydra with Dagster

Dagster is a data orchestration tool that makes it easy to build pipelines. Dagster provides a way to define "ops", which are units of computation that can be connected together to form a pipeline. Each op takes in inputs and produces outputs, which can be connected to other ops. Besides that, each op can be configured individually and independently of the other ops of the pipeline.

To use Hydra with Dagster, we can define a set of YAML files that define configuration settings for different parts of the pipeline. The default model training dagster training job is depicted below:

``` mermaid
graph LR
  experiment --> train;
  train --> prediction;
  prediction --> analysis;
  analysis --> exptests;
```

Each node in the graph represents one op. An example configuration file looks like this:

```yaml
# train binary classification  
defaults:  
  # experiment  
  - ops/experiment@ops.experiment.config: op_experiment_default.yaml  
  # train  
  - /ops/train@ops.train.config: op_train_cls_binary.yaml  
  # prediction  
  - /ops/prediction@ops.prediction.config: op_prediction_cls.yaml  
  # analysis  
  - /ops/analysis@ops.analysis.config: op_analysis_cls_binary.yaml  
  # exptests 
  - /ops/exptests@ops.exptests.config.tests: exptests_default.yaml  
  # experiment locations  
  - shared/locations@globals: exp_locations.yaml  
  - _self_  
  
hydra:  
  searchpath:  
    - file://configs  
  
globals:  
  exp_name: SampleClsBinary  
  exp_prefix: CLB  
  data_location:  
    uri: ${oc.env:DATA_URI,./data}/numbers_cropped_split
```


The `defaults` section specifies the loaded configurations for different operations:

- `ops/experiment`: specifies the configuration file for the experiment operation, which is `op_experiment_default.yaml`.
- `ops/train`: specifies the configuration file for the train operation for binary classification, which is `op_train_cls_binary.yaml`.
- `ops/prediction`: specifies the configuration file for the prediction operation for binary classification, which is `op_prediction_cls.yaml`.
- `ops/analysis`: specifies the configuration file for the analysis operation for binary classification, which is `op_analysis_cls_binary.yaml`.
- `ops/exptests`: specifies the configuration file for the experiment tests operation, which is `exptests_default.yaml`.
- `shared/locations`: specifies the configuration file for shared locations, which is `exp_locations.yaml`.
- `_self_`: specifies that the position at which the current file is included in the output configuration.

The `hydra` section sets the search path for the configuration files. Here, it specifies that the configuration files are located in the `configs` directory.

The `globals` section sets the global variables for the experiment. Here, it sets the experiment name to `SampleClsBinary`, experiment prefix to `CLB`, and the location of the data to `${oc.env:DATA_URI,./data}/numbers_cropped_split`. The `${oc.env:DATA_URI,./data}` means that the value of the `DATA_URI` environment variable is used if it exists, and if not, the default value is `./data`. The `uri` is a sub-key of `data_location` that specifies the URI for the data location.

This schema of imports is applied recursively which results in the following import graph.

``` mermaid
graph LR;

niceml/configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml(job_train_cls_binary) --> niceml/configs/ops/experiment/op_experiment_default.yaml(op_experiment_default);

niceml/configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml(job_train_cls_binary) --> niceml/configs//ops/train/op_train_cls_binary.yaml(op_train_cls_binary);

niceml/configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml(job_train_cls_binary) --> niceml/configs//ops/prediction/op_prediction_cls.yaml(op_prediction_cls);

niceml/configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml(job_train_cls_binary) --> niceml/configs//ops/analysis/op_analysis_cls_binary.yaml(op_analysis_cls_binary);

niceml/configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml(job_train_cls_binary) --> niceml/configs//ops/exptests/exptests_default.yaml(exptests_default);

niceml/configs/jobs/job_train/job_train_cls/job_train_cls_binary.yaml(job_train_cls_binary) --> niceml/configs/shared/locations/exp_locations.yaml(exp_locations);

niceml/configs//ops/train/op_train_cls_binary.yaml(op_train_cls_binary) --> niceml/configs//ops/train/op_train_base.yaml(op_train_base);

niceml/configs//ops/train/op_train_cls_binary.yaml(op_train_cls_binary) --> niceml/configs//shared/datasets/dataset_cls_test.yaml(dataset_cls_test);

niceml/configs//ops/train/op_train_base.yaml(op_train_base) --> niceml/configs//ops/train/callbacks/callbacks_base.yaml(callbacks_base);

niceml/configs//ops/train/op_train_base.yaml(op_train_base) --> niceml/configs//ops/train/train_params/trainparams_default.yaml(trainparams_default);

niceml/configs//ops/train/op_train_base.yaml(op_train_base) --> niceml/configs//ops/train/exp_initializer/exp_initializer_default.yaml(exp_initializer_default);

niceml/configs//ops/prediction/op_prediction_cls.yaml(op_prediction_cls) --> niceml/configs//shared/datasets/dataset_cls_test.yaml(dataset_cls_test);

niceml/configs//ops/prediction/op_prediction_cls.yaml(op_prediction_cls) --> niceml/configs//ops/prediction/prediction_handler/prediction_handler_vector.yaml(prediction_handler_vector);

niceml/configs//ops/prediction/op_prediction_cls.yaml(op_prediction_cls) --> niceml/configs//ops/prediction/datasets/datasets_generic_default.yaml(datasets_generic_default);

niceml/configs//ops/prediction/op_prediction_cls.yaml(op_prediction_cls) --> niceml/configs//ops/prediction/op_prediction_base.yaml(op_prediction_base);

niceml/configs/shared/locations/exp_locations.yaml(exp_locations) --> niceml/configs//shared/credentials/credentials_minio.yaml(credentials_minio);
```

One of the benefits of using a modular configuration system is that each component can be exchanged and configured independently, making it easier to test the entire system. As a result, all components and configurations can be tested individually, contributing to a more robust and reliable system overall.

### Op configuration

In Dagster, each op in a pipeline has its own configuration defined in the code. This configuration specifies the behavior of the op. 
In niceML we use this in combination with Hydra's instantiate feature to pass classes via configs to the ops. How each op should be 
configured you can find either in the source code or at our ops reference page.

!!! Hydra-instantiate-feature

    Hydra's instantiate feature allows you to create instances of Python classes specified in your configuration files using their fully-qualified name. This is useful when you want to pass instantiated objects to your application, such as passing a logger to a module or passing a database connection to your data layer.
    Hydra will look for the fully-qualified class name specified in your configuration and then use Python's import system to import and instantiate the class. You can also pass arguments to the class constructor by specifying them in the configuration.
    
    For example, if you have a Python class called `MyClass` in a module called `my_module`, you can instantiate it in your configuration file like this:
    
    ``` yaml
    my_class:
      _target_: my_module.MyClass
      arg1: value1
      arg2: value2
    ```
    
    When you use Hydra to load this configuration, it will create an instance of `MyClass` with `arg1` and `arg2` set to `value1` and `value2`, respectively.
    
    To do this, you can define a Python class that takes in the necessary configuration parameters and returns an instance of the op. This class can then be used as a config option for the op in your Dagster pipeline.



### Conclusion

In this tutorial, we've seen how to use Hydra with Dagster to configure a machine learning pipeline. Hydra allows for a hierarchical set of configuration files that can be used to define settings for different parts of the pipeline. 
The `defaults` section in the YAML file allows us to import the content of other YAML files, making it easy to reuse common settings across different parts of the pipeline.
