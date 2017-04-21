"""Model subclass for in memory predict functions"""

from .model import ModelType
from ..util import exceptions


class InMemoryModel(ModelType):
    """
    This model can be called directly from memory
    """

    def __init__(self, prediction_fn, log_level=30, class_names=None, examples=None):
        """This model can be called directly from memory
        Parameters
        ----------
        prediction_fn: callable
            function that returns predictions

        log_level: int
            config setting to see model logs. 10 is a good value for seeing debug messages.
            30 is warnings only.

        class_names: array type
            optional names of classes that describe model outputs.

        examples(numpy.array or pandas.dataframe):
            examples to use to make inferences about the function.
            prediction_fn must be able to take examples as an
            argument.
        """

        if not hasattr(prediction_fn, "__call__"):
            raise(exceptions.ModelError("Predict function must be callable"))

        self.prediction_fn = prediction_fn
        super(InMemoryModel, self).__init__(log_level=log_level,
                                            class_names=class_names,
                                            examples=examples)



    def predict(self, *args, **kwargs):
        """
        Just use the function itself for predictions
        """
        return self.formatter(self.prediction_fn(*args, **kwargs))


    @staticmethod
    def _predict(data, predict_fn, formatter):
        """Static prediction function for multiprocessing usecases

        Parameters
        ----------
        data: arraytype

        formatter: callable
            function responsible for formatting model outputs as necessary. For instance,
            one hot encoding multiclass outputs.

        predict_fn: callable

        Returns
        -----------
        predictions: arraytype
        """
        results = predict_fn(data)
        if formatter:
            return formatter(results)
        else:
            return results
