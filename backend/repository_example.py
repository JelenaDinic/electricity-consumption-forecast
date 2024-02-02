import datetime
import pandas as pd
from backend.weather_model import return_elements_from_database_in_range_predict
from backend.weather_model import return_all_elements
from datetime import date, timedelta
from backend.neural_network.custom_preparer import CustomPreparer
from backend.neural_network.ann_regression import AnnRegression
from backend.neural_network.custom_plotting import CustomPloting
from backend.neural_network.scorer import Scorer

NUMBER_OF_COLUMNS = 8
SHARE_FOR_TRAINING = 0.85

class Repo_example:

    @classmethod
    def upload_file_and_store(cls,file):
        
        data_frame = pd.read_csv(file)

        return True

    @classmethod
    def train_data(cls,start_date : date,end_date:date):
        elements = return_all_elements()
        preparer = CustomPreparer(elements, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING);
        trainX, trainY, testX, testY = preparer.prepare_for_training()
        ann_regression = AnnRegression()
        ann_regression.compile_fit_predict(trainX, trainY)
        return True

    @classmethod
    def predict_data(cls,start_date :date,days):
        if days > 7:
            return False
        end_date = start_date + timedelta(days - 1)
        elements = return_elements_from_database_in_range_predict(start_date, end_date)
        preparer = CustomPreparer(elements, NUMBER_OF_COLUMNS, 0)
        testX, testY = preparer.prepare_to_predict()
        # make predictions
        ann_regression = AnnRegression()
        testPredict  = ann_regression.compile_fit_predict_with_current_model(testX)
        testPredict, testY = preparer.inverse_transform_plot(testPredict)
        #calculate root mean squared error
        # scorer = Scorer()
        # testScore = scorer.get_absolute_test_score(testY, testPredict)
        # print('Test Score: %.2f RMSE' % (testScore))
        # plotting
        # custom_plotting = CustomPloting()
        # custom_plotting.show_plots(testPredict, testY)
        
        cls.store_to_csv(testPredict, start_date, days)
        return testPredict


    @classmethod
    def store_to_csv(cls, testPredict, start_date:datetime.date, days):
        ret_dict = {'date time': [] , 'load' : []}
        counter = 0
        date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
        for days in range(days):
            for hours in range(24):
                ret_dict['date time'].append(date.strftime('%Y-%m-%d %H:%M:%S'))
                ret_dict['load'].append(testPredict[counter])
                date = date + timedelta(hours=1)
                counter += 1

        df = pd.DataFrame(ret_dict)
        df.to_csv('predicted_values.csv')

