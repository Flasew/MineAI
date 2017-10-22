import tensorflow as tf

n_input = 300
n_hidden_1 = 256
n_hidden_2 = 128
n_output = 1
learning_rate = 0.001

class NN(object):

    def __init__(self):
        self.x = tf.placeholder("float", [None, n_input])
        self.y = tf.placeholder("float", [None, n_output])

        self.weights = {
            'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
            'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
            'out': tf.Variable(tf.random_normal([n_hidden_2, n_output]))
        }

        self.biases = {
            'b1': tf.Variable(tf.random_normal([n_hidden_1])),
            'b2': tf.Variable(tf.random_normal([n_hidden_2])),
            'out': tf.Variable(tf.random_normal([n_output]))
        }
        init = tf.global_variables_initializer()
        self.sess = tf.InteractiveSession()
        self.sess.run(init)
        self.avg_cost = 0.0

        # First Hidden layer with RELU activation
        layer_1 = tf.add(tf.matmul(self.x, self.weights['h1']), self.biases['b1'])
        layer_1 = tf.nn.relu(layer_1)

        # Second Hidden layer with RELU activation
        layer_2 = tf.add(tf.matmul(layer_1, self.weights['h2']), self.biases['b2'])
        layer_2 = tf.nn.relu(layer_2)

        # Last Output layer with linear activation
        self.pred = tf.nn.softmax(tf.matmul(layer_2, self.weights['out']) + self.biases['out'])
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.y))
        self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(self.cost)

    def predict(self, input_x):
        pred = self.sess.run(self.pred, feed_dict={self.x: input_x})
        return pred[0, 0]


    def train(self, batch_x, batch_y):
        _, c = self.sess.run([self.optimizer, self.cost], feed_dict={self.x: batch_x, self.y: batch_y})
        print(c)

if __name__ == '__main__':
    pass
