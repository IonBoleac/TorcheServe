# How to use and deploy a logreg model
All file are custom. You can use them as you want. And there is requirements.txt file for install all dependencies to register this project correctly in torchserve. This because the preprocess and postprocess in file [`logreg_handler.py`](logreg_handler.py) are custom and use pandas and numpy that are not installed by default in torchserve.
## How to archive this project
In first you need archive this project and install all dependencies. You can do it with this command:
```bash
torch-model-archiver --model-name logreg --version 2.0 --handler ./models_project/logreg/logreg_handler.py --model-file ./models_project/logreg/logreg_model.py --serialized-file ./models_project/logreg/logreg_parameters.pt --export-path ./model_store/ -f --requirements-file ./models_project/logreg/logreg_requirements.txt
```
In this case we use a requirements.txt file to install all dependencies needed to run model because it use a custom handler that use pandas and numpy and these dependencies are not installed by default in torchserve.
## How to deploy this project
In first you need deploy this project. **Obviously torchserve must be started.** You can do it with this command:
```bash
curl -X POST "http://localhost:8081/models?model_name=logreg&url=logreg.mar&batch_size=1&max_batch_delay=5000&initial_workers=1&synchronous=true"
```
## Test model with curl
You can test model with file head1.csv file using this command:
```bash
curl -X POST "http://localhost:8080/predictions/logreg" -T ./head1.csv
```
## Test model with python client
You can also test model with file head1.csv file using a client via this command:
```bash
cd models_project/logreg && python3 client.py
```
## PS
Be careful with the path and if you use docker you must bind the path of the model_store folder with the path of the model_store folder in the container and the path of all projects. This because when you archive a model in all options you designate paths of all files.