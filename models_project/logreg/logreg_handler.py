from ts.torch_handler.base_handler import BaseHandler
import logging, base64, io
from io import StringIO
import pandas as pd
from io import StringIO
import numpy as np
from torch.autograd import Variable
import torch, sys

logger = logging.getLogger(__name__)


class LogReg(BaseHandler):
    
    def __init__(self):
        super(LogReg, self).__init__()
        self.initialized = False
        self.manifest = None
        self.model = None
        self.device = None

    def preprocess(self, data):

        '''raw_data = []
        for row in data:
            logger.warning(f"preprocess row: {row}")
            # Compat layer: normally the envelope should just return the data
            # directly, but older versions of Torchserve didn't have envelope.
            row_line = row.get("data") or row.get("body")
            if isinstance(row_line, str):
                # 
                line = StringIO(row_line)
                pd.read_csv(line, index_col='id')

            # If the data is sent as bytesarray
            if isinstance(row_line, (bytearray, bytes)):
                line = row_line.decode('utf-8')
                pd_data = pd.read_csv(StringIO(line), sep=",", index_col='id')
                np_array = np.array(pd_data)
                variable_data = Variable(torch.FloatTensor(np_array), requires_grad=True)
                
            else:
                # if the data is a list
                #line = torch.FloatTensor(row)
                pass
            logger.warning(f"preprocess line: {type(line)}, {line}")
            
            raw_data.append(line)
        
        return line'''
        for raw in data:
            logger.warning(f"preprocess raw: {raw}")
            raw = raw.get("body") or raw.get("data")
            if (isinstance(raw, (bytearray, bytes))):
                line = raw.decode('utf-8')
                pd_data = pd.read_csv(StringIO(line), sep=",", index_col='id')
                np_array = np.array(pd_data)
                variable_data = Variable(torch.FloatTensor(np_array), requires_grad=True)
                torch_data = torch.FloatTensor(np_array)
                return variable_data
            if (isinstance(raw, str)):
                line = StringIO(raw)
                pd_data = pd.read_csv(line, sep=",", index_col='id')
                np_array = np.array(pd_data)
                variable_data = Variable(torch.FloatTensor(np_array), requires_grad=True)
                torch_data = torch.FloatTensor(np_array)
                return variable_data
        '''logger.warning(f"preprocess data: {data}, type {type(data)}")
        raw = data[0].get("body") or data[0].get("data")
        logger.warning(f"preprocess raw: {raw}, type {type(raw)}")
        line = raw.decode('utf-8')
        pd_data = pd.read_csv(StringIO(line), sep=",", index_col='id')
        np_array = np.array(pd_data)
        variable_data = Variable(torch.FloatTensor(np_array), requires_grad=True)
        torch_data = torch.FloatTensor(np_array)
        return variable_data'''
    
    '''def inference(self, data, *args, **kwargs):
        """
        The Inference Function is used to make a prediction call on the given input request.
        The user needs to override the inference function to customize it.

        Args:
            data (Torch Tensor): A Torch Tensor is passed to make the Inference Request.
            The shape should match the model input shape.

        Returns:
            Torch Tensor : The Predicted Torch Tensor is returned in this function.
        """
        
        with torch.no_grad():
            results = []
            for one in data:
                logger.warning(f"inference one: {one}")
                marshalled_data = one.to(self.device)
                result = self.model(marshalled_data, *args, **kwargs)
                results.append(result)
        
        results = torch.stack(results)
        logger.warning(f"inference results: {results}")
        return results'''
    
    def postprocess(self, data):
        data = super().postprocess(data)
        '''
        Args: 
            data (tensor): Data to be passed to postprocess function and converti it to list of dictionary.
        Returns:
            list: a list of a dictionary containing the prediction. Return must be a list big one that contains a dictionary or all tensors.
        '''
        logger.warning(f"postprocess data: {data}")
        re_results = []
        re_results.append({"predictions": data})

        # write a custom log line
        sys.stdout.write("re_results: " + str(re_results))
        return re_results
    
    


# torch-model-archiver --model-name logreg --version 2.0 --handler ./models_project/logreg/logreg_handler.py --model-file ./models_project/logreg/logreg_model.py --serialized-file ./models_project/logreg/logreg_parameters.pt --export-path ./model_store/ -f --requirements-file ./models_project/logreg/logreg_requirements.txt
# curl -X POST "http://localhost:8081/models?model_name=logreg&url=logreg.mar&batch_size=1&max_batch_delay=5000&initial_workers=1&synchronous=true"
# curl -X POST "http://localhost:8080/predictions/logreg" -T ./models_project/logreg/head1.csv
# curl http://localhost:8080/predictions/logreg --data-binary @./models_project/logreg/head1.csv -H 'Content-type:text/plain; charset=utf-8'