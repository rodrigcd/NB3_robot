import numpy as np
import demo_dl as dl
import data_funcs as df

batch_size = 20
num_epochs = 500
samples_per_class = 100
num_classes = 4
hidden_units = 100

data, target = df.gen_spiral_data(samples_per_class, num_classes, 0.2, 'double')
raw_data = df.plot_scatter(data, target)
raw_data.figure.savefig("demo_raw.png")

model = dl.Model()
model.add(dl.Linear(2, hidden_units))
model.add(dl.ReLU())
model.add(dl.Linear(hidden_units, num_classes))
optimiser = dl.SGD(model.parameters, lr=1, weight_decay=0.001, momentum=0.9)
loss = dl.sigmoid()
model.fit(data, target, batch_size, num_epochs, optimiser, loss, df.data_generator)
pre_arg = model.predict(data)

pred_labels = np.argmax(pre_arg, axis=1)
good_labels = pred_labels == target
accuracy = np.mean(good_labels)
print("model Accuracy = {:.2f}%".format(accuracy*100))
classified_data = df.plot_decision(data, target, model)
classified_data.figure.savefig("demo_classified.png")
