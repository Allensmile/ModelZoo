import tensorflow as tf
from model_zoo.utils import load_config, get_shape, load_model

tfe = tf.contrib.eager
tf.enable_eager_execution()

tf.flags.DEFINE_string('checkpoint_dir', 'checkpoints', help='Data source dir', allow_override=True)
tf.flags.DEFINE_string('checkpoint_name', 'model.ckpt', help='Model name', allow_override=True)


class BaseInferer():
    """
    Base Inferer, you need to specify
    """
    
    def __init__(self):
        """
        you need to define model_class in your Inferer
        """
        self.model_class = None
        self.flags = tf.flags.FLAGS
    
    def prepare_data(self):
        """
        you need to implement this method
        :return:
        """
        raise NotImplementedError
    
    def run(self):
        """
        start inferring
        :return:
        """
        # get test_data
        self.test_data = self.prepare_data()
        # init model
        model = self.model_class(load_config(self.flags))
        model.init()
        # init variables
        model.call(tf.keras.Input(shape=(get_shape(self.test_data))), training=False)
        # restore model if exists
        load_model(model, self.flags.checkpoint_dir, self.flags.checkpoint_name)
        # infer
        return model.infer(self.test_data)
