# ModelZoo

A framework to help you build model much more easily.

## Installation

You can install this package easily with pip:

```
pip3 install model-zoo
```

## Usage

Let's implement a linear-regression model quickly.

Here we use boston_housing dataset as example.

Define a linear model like this, named `model.py`:

```python
from model_zoo.model import BaseModel
import tensorflow as tf

class BostonHousingModel(BaseModel):
    def __init__(self, config):
        super(BostonHousingModel, self).__init__(config)
        self.dense = tf.keras.layers.Dense(1)

    def call(self, inputs, training=None, mask=None):
        o = self.dense(inputs)
        return o

```

Then define a trainer like this, named `train.py`:

```python
from model import BostonHousingModel
from model_zoo.trainer import BaseTrainer
from tensorflow.python.keras.datasets import boston_housing
from sklearn.preprocessing import StandardScaler

class Trainer(BaseTrainer):

    def __init__(self):
        BaseTrainer.__init__(self)
        self.model_class = BostonHousingModel

    def prepare_data(self):
        (x_train, y_train), (x_eval, y_eval) = boston_housing.load_data()
        ss = StandardScaler()
        ss.fit(x_train)
        x_train, x_eval = ss.transform(x_train), ss.transform(x_eval)
        train_data, eval_data = (x_train, y_train), (x_eval, y_eval)
        return train_data, eval_data

if __name__ == '__main__':
    Trainer().run()
```

Now, we've finished this model.

Next we can run this model like this:

```
python3 train.py
```

Outputs like this:

```
Epoch 1/100
 1/13 [=>............................] - ETA: 0s - loss: 816.1798
13/13 [==============================] - 0s 4ms/step - loss: 457.9925 - val_loss: 343.2489

Epoch 2/100
 1/13 [=>............................] - ETA: 0s - loss: 361.5632
13/13 [==============================] - 0s 3ms/step - loss: 274.7090 - val_loss: 206.7015
Epoch 00002: saving model to checkpoints/model.ckpt

Epoch 3/100
 1/13 [=>............................] - ETA: 0s - loss: 163.5308
13/13 [==============================] - 0s 3ms/step - loss: 172.4033 - val_loss: 128.0830

Epoch 4/100
 1/13 [=>............................] - ETA: 0s - loss: 115.4743
13/13 [==============================] - 0s 3ms/step - loss: 112.6434 - val_loss: 85.0848
Epoch 00004: saving model to checkpoints/model.ckpt

Epoch 5/100
 1/13 [=>............................] - ETA: 0s - loss: 149.8252
13/13 [==============================] - 0s 3ms/step - loss: 77.0281 - val_loss: 57.9716
....

Epoch 42/100
 7/13 [===============>..............] - ETA: 0s - loss: 20.5911
13/13 [==============================] - 0s 8ms/step - loss: 22.4666 - val_loss: 23.7161
Epoch 00042: saving model to checkpoints/model.ckpt
```

It runs only 42 epochs and stopped early, because there are no more good evaluation results for 20 epochs.

When finished, we can find two folders generated named `checkpoints` and `events`.

Go to `events` and run TensorBoard:

```
cd events
tensorboard --logdir=.
```

TensorBoard like this:

![](https://ws4.sinaimg.cn/large/006tNbRwgy1fvxrcajse2j31kw0hkgnf.jpg)

There are training batch loss, epoch loss, eval loss.

And also we can find checkpoints in `checkpoints` dir.

It saved the best model named `model.ckpt` according to eval score, and it also saved checkpoints every 2 epochs.

Next we can predict using existing checkpoints, define `infer.py` like this:

```python
from model import BostonHousingModel
from model_zoo.inferer import BaseInferer
import tensorflow as tf
from tensorflow.python.keras.datasets import boston_housing
from sklearn.preprocessing import StandardScaler

tf.flags.DEFINE_string('checkpoint_name', 'model.ckpt-38', help='Model name')

class Inferer(BaseInferer):
    def __init__(self):
        BaseInferer.__init__(self)
        self.model_class = BostonHousingModel

    def prepare_data(self):
        (x_train, y_train), (x_test, y_test) = boston_housing.load_data()
        ss = StandardScaler()
        ss.fit(x_train)
        x_test = ss.transform(x_test)
        return x_test


if __name__ == '__main__':
    result = Inferer().run()
    print(result)
```

Now we've restored the specified model `model.ckpt-38` and prepared test data, outputs like this:

```python
[[ 9.637125 ]
 [21.368305 ]
 [20.898445 ]
 [33.832504 ]
 [25.756516 ]
 [21.264557 ]
 [29.069794 ]
 [24.968184 ]
 ...
 [36.027283 ]
 [39.06852  ]
 [25.728745 ]
 [41.62165  ]
 [34.340042 ]
 [24.821484 ]]
```

OK, we've finished restoring and predicting. Just so quickly.

## License

MIT