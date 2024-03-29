from keras.layers import Dense, Dropout
from keras.models import Sequential
from tensorflow import keras
from neural_network.ann_base import AnnBase

MODEL_TEST = 'test_model_name'


class AnnRegression(AnnBase):


    def get_model(self):
        model = Sequential()
        if self.number_of_hidden_layers > 0:
           model.add(Dense(self._number_of_neurons_in_first_hidden_layer, input_shape=(1, 7), kernel_initializer=self.kernel_initializer, activation=self.activation_function))
           if self.number_of_hidden_layers > 1:
               for i in range(self.number_of_hidden_layers - 1):
                   model.add(Dense(self.number_of_neurons_in_other_hidden_layers, kernel_initializer=self.kernel_initializer, activation=self.activation_function))
        model.add(Dense(1, kernel_initializer=self.kernel_initializer))
        return model

    def get_model_from_path(self, path):
        model = keras.models.load_model(path)
        return model


    def compile_and_fit(self, trainX, trainY):
        self.model = self.get_model()
        self.model.compile(loss=self.cost_function, optimizer=self.optimizer)
        self.trainX = trainX
        
        self.model.fit(trainX, trainY, epochs=self.epoch_number, batch_size=self.batch_size_number, verbose=self.verbose)
        self.model.save(MODEL_TEST)


    def use_current_model(self, path, trainX):
        self.trainX = trainX
        self.model = self.get_model_from_path(path)

    def get_predict(self, testX):
        testPredict = self.model.predict(testX)
        return testPredict

    def compile_fit_predict_with_current_model(self, testX):
        self.model = self.get_model_from_path(MODEL_TEST)
        return self.get_predict(testX)

    def compile_fit_predict(self, trainX, trainY):
        self.compile_and_fit(trainX, trainY)

