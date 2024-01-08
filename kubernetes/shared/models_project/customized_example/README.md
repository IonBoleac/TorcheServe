# How to create and run a simple example
This model is a simple model that classifies images of clothes in 10 classes. The model is trained with the dataset [FashionMNIST](https://www.kaggle.com/datasets/zalando-research/fashionmnist). <br></br>
All things in this example are customized. There are some files:
- `model.py`: contains the arch's model
- `handler.py`: contains the handler that manage your data thus handles pre-processing-post of data
- `parameters.pt`: contains the state_dict of the model created with `torch.save(model.state_dict(), 'parameters.pt')`
- `checkpoint.pt`: contains the checkpoint of the model created with `torch.save(model, 'checkpoint.pt')`
- `script_module.pt` and `trace_module.pt`: are two files created respectively by `torch.jit.script(model, 'script_module.pt')` and `torch.jit.trace(model, 'trace_module.pt')` that are used in case of TorchScript mode
## 1. Create a new archiver in EagerMode
```bash
torch-model-archiver -f --model-name fashion --version 1.0 --handler ./models_project/customized_example/handler.py --model-file ./models_project/customized_example/model.py --serialized-file ./models_project/customized_example/parameters.pt --export-path ./model_store/ 
```
## 2. Run the Torchserve
```bash
torchserve --start --model-store model_store --ncs
```
## 3. Register the model
```bash
curl -X POST "http://localhost:8081/models?url=fashion.mar&model_name=fashion&model_version=1.0&batch_size=1&max_batch_delay=5000&initial_workers=1&synchronous=true"
```
## 4. Get an inference from Torchserve
In directory `/img` there are some images that you can use to test the model. You can use `curl` to get an inference from Torchserve:
```bash
curl -X POST "http://localhost:8080/predictions/fashion" -T ./customized_example/img/test1.png
```
If you want use file `download.ipynb` to download other images from the web. In first you have to install `jupyter` and `ipykernel`.  


