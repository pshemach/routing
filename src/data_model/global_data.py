from src.data_model.data_model import create_data_model

data = create_data_model()

def reset_global_data():
    """ Reset the global data model to default """
    global data
    data = create_data_model()
