from src.data_model.data_model import create_data_model

data = create_data_model(distance_matrix=[[1,2], [3,4]], locations=['A', 'B'])

print("Okay,")
print(data)
