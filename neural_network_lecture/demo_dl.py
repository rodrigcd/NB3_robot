import numpy as np

class function(object):
    def forward(self):
        raise NotImplementedError

    def backward(self):
        raise NotImplementedError

    def get_params(self):
        return []

class optimiser(object):
    def __init__(self, parameters):
        self.parameters = parameters

    def step(self):
        raise NotImplementedError

    def zero_grad(self):
        for p in self.parameters:
            p.grad=0

class tensor:
    def __init__(self, dimensions):
        self.data = np.ndarray(dimensions, np.float32)
        self.grad = np.ndarray(dimensions, np.float32)
        self.size = dimensions

class Linear(function):
    def __init__(self, in_nodes, out_nodes):
        self.weights = tensor((in_nodes, out_nodes))
        self.bias = tensor((1, out_nodes))
        self.type = 'linear'

    def forward(self, x):
        output = np.dot(x, self.weights.data) + self.bias.data
        self.input = x
        return output

    def backward(self, d_y):
        self.weights.grad += np.dot(self.input.T, d_y)
        self.bias.grad += np.sum(d_y, axis=0, keepdims=True)
        grad_input = np.dot(d_y, self.weights.data.T)
        return grad_input

    def get_params(self):
        return (self.weights, self.bias)

class sigmoid(function):
    def __init__(self):
        self.type = 'normalization'

    def forward(self, x, target):
        unnormalized_prob = np.exp(x-np.max(x, axis=1, keepdims=True))
        self.prob = unnormalized_prob/np.sum(unnormalized_prob, axis=1, keepdims=True)
        self.target = target
        loss = -np.log(self.prob[range(len(target)), target])
        return loss.mean()

    def backward(self):
        gradient = self.prob
        gradient[range(len(self.target)), self.target] -= 1.0
        gradient/=len(self.target)
        return gradient

class ReLU(function):
    def __init__(self):
        self.type = 'Activation'

    def forward(self, x):
        self.activated = x*(x>0)
        return self.activated

    def backward(self, d_y):
        return d_y*(self.activated > 0)

class SGD(optimiser):
    def __init__(self, parameters, lr=1, weight_decay=0.0, momentum=0.9):
        super().__init__(parameters)
        self.lr = lr
        self.weight_decay = weight_decay
        self.momentum = momentum
        self.velocity = []
        for p in parameters:
            self.velocity.append(np.zeros_like(p.grad))

    def step(self):
        for p,v in zip(self.parameters, self.velocity):
            v = self.momentum*v + p.grad + self.weight_decay*p.data
            p.data = p.data - self.lr*v


class Model():
    def __init__(self):
        self.computation_graph = []
        self.parameters = []

    def add(self, layer):
        self.computation_graph.append(layer)
        self.parameters += layer.get_params()

    def __initialiseNet(self):
        for f in self.computation_graph:
            if f.type == 'linear':
                weights, bias = f.get_params()
                weights.data = 0.01*np.random.randn(weights.size[0], weights.size[1])
                bias.data = 0.0

    def fit(self, data, target, batch_size, num_epochs, optimiser, loss_fn, data_gen, print_int=100):
        loss_history = []
        self.__initialiseNet()
        data_gen = data_gen(data, target, batch_size)
        itr = 0
        for epoch in range(num_epochs):
            for X, Y in data_gen:
                optimiser.zero_grad()
                for f in self.computation_graph:
                    X = f.forward(X)
                loss = loss_fn.forward(X, Y)
                grad = loss_fn.backward()
                for f in self.computation_graph[::-1]:
                    grad = f.backward(grad)
                loss_history += [loss]
                if np.mod(itr, print_int) == 0:
                    print("Epoch = {}, iteration= {}, loss={}".format(epoch, itr, loss_history[-1]))
                itr += 1
                optimiser.step()

    def predict(self, data):
        X = data
        for f in self.computation_graph:
            X = f.forward(X)
        return X























