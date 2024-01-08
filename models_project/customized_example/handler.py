from ts.torch_handler.base_handler import BaseHandler
from torchvision import transforms
import torch
from model import Model
from PIL import Image
import logging
import base64
import io

logger = logging.getLogger(__name__)


class MNISTFashionClassifier(BaseHandler):

    
    
    def __init__(self):
        super(MNISTFashionClassifier, self).__init__()
        self.initialized = False
        # Define a transform to normalize the data
        self.transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize((0.5,), (0.5,))])

    def initialize(self, context):
        '''
        Invoke by torchserve for loading a model
        :param context: context contains model server system properties
        :return:
        '''
        # maybe this def is not necessary
        super(MNISTFashionClassifier, self).initialize(context)
        self.manifest = context.manifest
        properties = context.system_properties
        self.device = torch.device("cuda:" + str(properties.get("gpu_id"))
                                    if torch.cuda.is_available() and properties.get("gpu_id") is not None
                                    else "cpu")
        model_dir = properties.get("model_dir")
        self.__context = context

        self.initialized = True

        '''self.model = Model()
        self.model.load_state_dict(torch.load(f"{model_dir}/{super().model_pt_path}"))'''


    
    def preprocess(self, data):
        #data is a list. In fact you may receive a list of images to be processed.
        #super().preprocess(data)
        #logger.warning("Preprocessing data ", data)
        # Compat layer: normally the envelope should just return the data
        # directly, but older versions of Torchserve didn't have envelope.
        images = []

        for row in data:
            logger.warning(f"preprocess row: {row}")
            # Compat layer: normally the envelope should just return the data
            # directly, but older versions of Torchserve didn't have envelope.
            image = row.get("data") or row.get("body")
            if isinstance(image, str):
                # if the image is a string of bytesarray.
                image = base64.b64decode(image)

            # If the image is sent as bytesarray
            if isinstance(image, (bytearray, bytes)):
                image = Image.open(io.BytesIO(image))
                
            else:
                # if the image is a list
                image = torch.FloatTensor(image)
            
            image = self.transform(image)
            images.append(image)


        
        # Process the input data
        # The data that you send is must be in the form like you model accept them as input.
        # in this case my model accept a tensor of size (1, 784) as input so I have to reshape the input data
        # qua ritorno solamente l'ultima immagine della lista foramttata come tensor
        return image.view(1, 784)
    

    def postprocess(self, data):
        post_data = super().postprocess(data)
        logger.warning(f"postprocess data: {post_data}, type {type(post_data)}")
        return post_data
    


    
