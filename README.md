# TorchServe
<img src="img/principal_img.jpg" 
      style="display: block; 
            margin-left: auto;
            margin-right: auto;
            width: 100%;"></img><br></br>
This is a serving platform for **PyTorch** models in localhost
If you want to use docker or k8s you must install docker and k8s first. To do so, it's recommended to follow this [link](https://github.com/alessandrogilli/lab-k8s) to install k8s and this [link](https://www.docker.com/products/docker-desktop/) to install docker on window. In this repo there are a [guide step-by-step](kubernetes/README) how to deploy torchserve on kubernetes cluster.

## 1) Installation
1. Clone the official repository of torchserve
```bash
git clone git@github.com:pytorch/serve.git
```
2. Go to the directory of torchserve cloned repository
```bash
cd serve
```
3. Install dependencies. See [official site](https://pytorch.org/serve/getting_started.html) for more.
```bash
# Install dependencies
# If you want to use gpu, you must install cuda first
# cuda is optional
python3 ./ts_scripts/install_dependencies.py #--cuda=...
```
Another option is to install only `java` with command for more supervision:
```bash
sudo apt install openjdk-17-jdk
```
4. Install `torchserve` and `torch-model-archiver` (you can do this step in Python virtual environment).
```bash
# Install torchserve
pip3 install -r simple_req.txt
```

## 2) Usage torch-model-archiver and torchserve
1. Go to the directory of your project and run this command to create a [model archive](https://github.com/pytorch/serve/blob/master/model-archiver/README.md). You should specify the name of your model, its version, its path to the serialized file, its handler, the path to the export `.mar` file, the path to the extra files - if you have any - and other options if you want them to be explained in the official repository of torchserve or in my documentation. Moreover, you should obviously create your serialized file, your handler, your model and your extra files before running this command and other extra files - if you have any - before running this command. You should use standard torchserve handler or [custom handler](https://github.com/pytorch/serve/blob/master/docs/custom_service.md#custom-handlers) and if you want to use custom handler, you should create it first, together with other custom file. You can see an example of creating a [model archive](https://github.com/pytorch/serve/blob/master/model-archiver/README.md) in the next section.
```bash
torch-model-archiver --model-name <model-name> --version <version_of the model> --serialized-file <path-to-serialized_file> --handler <handler> --export-path <path-to-export-.mar-file> --extra-files <path-to-extra-files> # and other options if you want that are explained in the official repository of torchserve or in my documentation
```
### 2.1) Example on how to create a custom handler and other custom files
Firstly, you have to know in which mode you should realize your model. There are two options: Eager mode or Torchscript mode. In this repo Eager Mode is used.
- Create a file `.py` that will be used as a model handler. This file may manage the pre-processing, procesing and post-processing of the inference of the data. Furthermore, this file can extend the [standard handler](https://pytorch.org/serve/default_handlers.html) class. You can see an example of the creation of a custom handler in the next section that extends [`ImageClassifier`](https://pytorch.org/serve/default_handlers.html#image-classifier) class and that handles only The postprocessing of data. You can see the [official repository](https://pytorch.org/serve/custom_service.html#custom-handlers) of torchserve or my documentation for more info.
```python
from torchvision import transforms
from ts.torch_handler.image_classifier import ImageClassifier
from torch.profiler import ProfilerActivity


class MNISTDigitClassifier(ImageClassifier):
    """
    MNISTDigitClassifier handler class. This handler extends class ImageClassifier from image_classifier.py, a
    default handler. This handler takes an image and returns the number in that image.

    Here method postprocess() has been overridden while others are reused from parent class.
    """

    image_processing = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    def __init__(self):
        super(MNISTDigitClassifier, self).__init__()
        self.profiler_args = {
            "activities" : [ProfilerActivity.CPU],
            "record_shapes": True,
        }


    def postprocess(self, data):
        """The post process of MNIST converts the predicted output response to a label.

        Args:
            data (list): The predicted output from the Inference with probabilities is passed
            to the post-process function
        Returns:
            list : A list of dictionaries with predictions and explanations is returned
        """
        return data.argmax(1).tolist()
```
- You can use a model from [models zoo](https://pytorch.org/serve/model_zoo.html) or you can create and use your own model. This file defines the model's arch and it's mandatory in Eager mode and contains the extended class from `torch.nn.Module`. You can see an example of creating a model in the next section.
```python
import torch
from torch import nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)
        self.dropout2 = nn.Dropout2d(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output
```

2. Now create a directory named `model_store` in the directory of your project and copy the `.mar` file in it. IMPORTANT: You must never delete model_store directory because it is used as a model store of torchserve. In addition, don't use the subfolder in this directory.
```bash
mkdir model_store
cp <path-to-.mar-file> model_store
```
2. Now you can run torchserve an register your model together with starting it or you should register your `<file-name>.mar` file after using Management APIs of torchserve. You can see an example of running torchserve in the next section. Check the official repository of torchserve or my documentation for more.
```bash
torchserve --start --model-store model_store --models <model-name>=<model-name>.mar --log-config <path-to-log-config-file> # other options if you want
```
3. Now you can send a request to your model using endpoints (Inference APIs) of torchserve served on port `8080` by default. See this [link](https://curl.se/docs/manpage.html) to under stand how to use curl. You can use other endpoint and methods to send a request to your model, if you want.
```bash
curl -X GET "http://localhost:8080/predictions/<model-name>" -T <path-to-date-to-do-inference>
# or
curl -X POST "http://localhost:8080/predictions/<model-name>" -T <path-to-date-to-do-inference>
```
4. You can stop torchserve using this command
```bash
torchserve --stop
```

## 3) [Example on how to create a model archive and use it on localhost](how_to_load_models.md) 
1. Create .mar file of mnist model in this repository used as an example (source of this model is [here](https://github.com/pytorch/serve/tree/master/examples/image_classifier/mnist)). This comand creates a `.mar` file named `mnist.mar` in the directory `model_store` that will be used as a model store of torchserve. ***IMPORTANT:*** You must never delete `model_store` directory because it is used as a model store of torchserve.
```bash
torch-model-archiver --model-name mnist --version 1.0 --handler ./models_project/mnist/mnist_handler.py --model-file ./models_project/mnist/mnist.py --serialized-file ./models_project/mnist/mnist_cnn.pt --export-path ./model_store/ --extra-files ./models_project/mnist/mnist_ts.json
```
2. Now you can run torchserve and if want you can register your model together with starting torchserve using bottom command. 
```bash
torchserve --start --model-store model_store --ts-config config.properties --models mnist=model_store/mnist.mar
```
3. Now move to the directory model_store and register your first model using this command. If you want [there](https://pytorch.org/serve/model_zoo.html) are models zoo. You can see an example on how to create a model archive in the next section.
```bash
cd model_store
curl -X POST "http://localhost:8081/models?model_name=mnist&url=mnist.mar&batch_size=1&max_batch_delay=5000&initial_workers=1&synchronous=true"
```
After that, The system will return you a response like this
```bash
{
  "status": "Model \"mnist\" Version: 1.0 registered with 1 initial workers"
}
```
4. To test if your model is registered correctly, you can send a request to your model using endpoints (Inference APIs) of torchserve served on port 8080 by default 
```bash
curl -X POST "http://localhost:8080/predictions/mnist" -T ./mnist/test_data/0.png
```
After THAT, The system will return you a response with 0 because the `image 0.png` is an image of 0 digit

5. Now you can use your model on localhost.

## 4) Example on how to run torchserve on docker
*For that you have not to install all package in requirments file because the image of torchserve has already installed all needed packages. You must install only `torch-model-archiver` and `torch-workflow-archiver` if you use workflow that are used to create `.mar` file.*
1. Follow the first step of the previous example
2. Now you can run torchserve on docker using this command (you can bind gRPC ports if you want). You must bind your local directory `model_store` to the directory `/home/model-server/model-store` in the container because this directory is used as a model store of torchserve. You must bind as a volume all your files that are used to serve your models. <br></br> IMPORTANT: You must never delete binded volume because they are used.
```bash
docker run --rm -it -p 127.0.0.1:8080:8080 -p 127.0.0.1:8081:8081 -p 127.0.0.1:8082:8082 -v $(pwd)/model_store:/home/model-server/model-store -v $(pwd)/models_project:/home/model-server/models_project -v $(pwd)/docker_config.properties:/home/model-store/config.properties --env-file $(pwd)/ENV.env pytorch/torchserve:latest-cpu
```
Or you can use a minimal compose-file situated in this project that create and a prometheus container. You can custom this file for your needs. To do that you should run the following command.
```bash
docker compose up 
```
3. Now you should register your model if you don't register it with starting torchserve. After that, you can test if it works correctly using the same command as in the previous example. To do that you should follow steps 3 and 4 of the previous example. There are other APIs that you can run to contact torchserve ([Management APIs](https://github.com/pytorch/serve/blob/master/docs/management_api.md)) and your registered model ([Inference APIs](https://github.com/pytorch/serve/blob/master/docs/inference_api.md)). 

<br></br>
PS. In this repo there are ENV file that you can custom with your needs. You can see the [official repository](https://pytorch.org/serve/configuration.html).

## 5) Example how to configure metrics and how to use them via Management APIs
***IMPORTANT!!!*** Don't confuse this with custom Metris API. This is a different thing. You can see the [official repository](https://github.com/pytorch/serve/blob/master/docs/metrics.md) of Metrics's configuration and use.
  1. Firstly, you should configure the file `config.properties` to use your custom metrics. To do that you should add the following lines to the file `config.properties`.
  ```properties
  metrics_config=/<path>/<to>/<metrics>/<file>/metrics.yml
  metrics_mode=log
  # or if you want to use prometheus set
  metrics_mode=prometheus
  ```
  Or you can add the bottom option to the command line when you start torchserve.
  ```bash
  --metrics-config=path-to-file-config.yml 
  ```
  Based on your choice you can use log file or Prometheus binded with Grafana (by APIs) to see your metrics. 

  An example of a `config-mtrics.yml` is
  ```yaml
  dimensions: # dimension aliases
    - &model_name "ModelName"
    - &level "Level"

  ts_metrics:  # frontend metrics
    counter:  # metric type
      - name: NameOfCounterMetric  # name of metric
        unit: ms  # unit of metric
        dimensions: [*model_name, *level]  # dimension names of metric (referenced from the above dimensions dict)
    gauge:
      - name: NameOfGaugeMetric
        unit: ms
        dimensions: [*model_name, *level]
    histogram:
      - name: NameOfHistogramMetric
        unit: ms
        dimensions: [*model_name, *level]

  model_metrics:  # backend metrics
    counter:  # metric type
      - name: InferenceTimeInMS  # name of metric
        unit: ms  # unit of metric
        dimensions: [*model_name, *level]  # dimension names of metric (referenced from the above dimensions dict)
      - name: NumberOfMetrics
        unit: count
        dimensions: [*model_name]
    gauge:
      - name: GaugeModelMetricNameExample
        unit: ms
        dimensions: [*model_name, *level]
    histogram:
      - name: HistogramModelMetricNameExample
        unit: ms
        dimensions: [*model_name, *level]
  ```
2. After that you may read file log or request metrics via Management APIs in based on your choice. To request metrics via Management APIs you should use the following command. You can see the [official repository](https://pytorch.org/serve/metrics_api.html).
    ```bash
    curl http://127.0.0.1:8082/metrics
    ```
3. If you want to use Prometheus binded with Grafana (by APIs) to see your metrics, before that you appropriately configure them. 
    ### 5.1) Example how to configure custom metrics APIs for backend metrics
    You can write your [custom metrics API](https://github.com/pytorch/serve/blob/master/docs/metrics.md#custom-metrics-api). 
    <br></br>
    ***IMPORTANT:*** Don't confuse this with [Metrics API endpoint](https://pytorch.org/serve/metrics_api.html) which is used to fetch metrics in the prometheus format. 
    <br></br>
    In this case you should custom your `config-mtrics.yml` like example on the top and configure your custom handler like this:
    ```python
    def CustomHanlder(BaseHandler):
      def initialize(self, context):
              super().initialize(context)
              metrics = context.metrics  # initializing metrics to the context.metrics
              # create new dimensions
              
              __dimensions = []
              __dimensions.append(Dimension(name="MyName", value="MNIST"))
              __dimensions.append(Dimension(name="MyLevel", value="Level1"))
              


              # create new metrics
              metric = metrics.add_metric(name="NumberOfPredictions", metric_type=MetricTypes.COUNTER, value=0, unit="count", dimensions=__dimensions)

    ```
    And your custom `metrics-config.yaml` file like this:
    ```yaml
    dimensions:
      - &model_name "ModelName"
      - &worker_name "WorkerName"
      - &level "Level"
      - &device_id "DeviceId"
      - &hostname "Hostname"
      - &my_name "MyName"
      - &my_level "MyLevel"

    model_metrics:
      counter:
        - name: NumberOfPredictions
          unit: count
          dimensions: [*my_name, *my_level, *hostname]
    # Dimension "Hostname" is automatically added for model metrics in the backend
      gauge:
        - name: HandlerTime
          unit: ms
          dimensions: [*model_name, *level]
        - name: PredictionTime
          unit: ms
          dimensions: [*model_name, *level]
    ```
    Whene you write your custom metrics API, you should create your archive and run torchserve like in the previous example. After that you can read your custom metrics API via Management APIs or in log file, depend how it's set `metrics_mode` in `config.properties` file. You can see the [official repository](https://pytorch.org/serve/metrics.html#custom-metrics-api) of Metrics's configuration and use.

    ### 5.2) Example how to request metrics via Management APIs
    You can request metrics via Management APIs that pull all available metrics on port `8082` or in the log file, based on your chois per `metrics_mode`. For that you should use the following command. You can see the [official repository](https://pytorch.org/serve/metrics_api.html).
    ```bash
    curl http://localhost:8082/metrics
    ```
    This command will return you a response like this: 
    ```bash
    # HELP ts_model_metric_InferenceTimeInMS_ms InferenceTimeInMS
    # TYPE ts_model_metric_InferenceTimeInMS_ms histogram
    ts_model_metric_InferenceTimeInMS_ms_bucket{model_name="mnist",level="model",le="0.005"} 0.0
    ```
    ### 5.3) Example how to configure Prometheus and Grafana to see metrics
## 6) Advanced configuration
1. You may confige your entire torchserve's config by custom config file. For that you should add option in the bottom in your `config.properties` file or use envoriorment var `$TS_CONFIG_FILE=/path-to-<config.properties>-file`.
    ```bash
    --ts-config=/path-to-<config.properties>-file
    ```
    to the command line when you start torchserve. You can see an example of config.properties file in this repo there are some examples. For more info you can see all options of `config.properties` file in the [official repository](https://github.com/pytorch/serve/blob/master/docs/configuration.md) of torchserve or in my documentation.

    PS. In the directory [`./models_project/customized_example`](./models_project/customized_example/) there are some files with which you can see how to create a custom project.

### Ps.
Be ***careful*** with the paths and if you use containers you must bind the path of the model_store folder with the path of the model_store folder in the container and the paths of all projects. This because when you archive a model in all options you designate only the paths of all files.

### Cite
I used the official repo to create this documentation. You can see the [official repository](https://github.com/pytorch/serve) of torchserve for more info.