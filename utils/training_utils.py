from keras.models import Model
from keras.layers import Dropout, Dense, Input, BatchNormalization
from keras.applications.efficientnet_v2 import EfficientNetV2S

def build_model(weight_path, print_summary=False):
    input_shape = (100,100,3)
    EffNet = EfficientNetV2S(
        include_top=False,
        weights=None,
        input_tensor=None,
        input_shape=input_shape,
        pooling='max',
        classes=None,
        classifier_activation=None,
        include_preprocessing=False
    )


        
    input1 = Input(shape=input_shape)
    x = EffNet(input1)
    x = Dense(256)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Dense(128)(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Dense(units=7,activation='softmax')(x)
    model = Model(input1, x)   

    #backbone = model.layers[1]
    model.load_weights(weight_path)
    #backbone.trainable = False
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


    if print_summary:
        model.summary()
        
    return model