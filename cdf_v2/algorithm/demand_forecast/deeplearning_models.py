#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-25 16:08:32
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import sys
import numpy as np
from numpy import *
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators.estimator import SKCompat
if sys.version_info[0] == 3:
    from functools import reduce

import warnings
warnings.filterwarnings("ignore")

# 导入自定义的包
from algorithm.demand_forecast.feature_engineering import *

class dp_LSTM:
	"""
	Parameters
	------------
	Attributes
	------------
	"""
	def __init__(self,HIDDEN_SIZE=55,NUM_LAYERS=3,BATCH_SIZE=30,TRAINING_STEPS=3000,
		learning_rate=0.01,optimizer ='Adagrad'):
		# 神经网络参数
		self.HIDDEN_SIZE = HIDDEN_SIZE  # LSTM隐藏节点个数
		self.NUM_LAYERS  = NUM_LAYERS   # LSTM层数
		self.BATCH_SIZE  = BATCH_SIZE   # batch大小
		# 数据参数
		self.TRAINING_STEPS = TRAINING_STEPS  # 训练轮数
		self.learning_rate = learning_rate # 学习率
		self.optimizer = optimizer
		self.regressor=None

	# LSTM结构单元
	def LstmCell(self):
		lstm_cell = tf.contrib.rnn.BasicLSTMCell(self.HIDDEN_SIZE)
		return lstm_cell

	def lstm_model(self,X, y):
		# 使用多层LSTM，不能用lstm_cell*NUM_LAYERS的方法，会导致LSTM的tensor名字都一样
		cell = tf.contrib.rnn.MultiRNNCell([self.LstmCell() for _ in range(self.NUM_LAYERS)])
		# 将多层LSTM结构连接成RNN网络并计算前向传播结果
		output, _ = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
		output = tf.reshape(output, [-1, self.HIDDEN_SIZE])
		# 通过无激活函数的全联接层计算线性回归，并将数据压缩成一维数组的结构
		predictions = tf.contrib.layers.fully_connected(output, 1, None)
		# 将predictions和labels调整为统一的shape
		y = tf.reshape(y, [-1])
		predictions = tf.reshape(predictions, [-1])
		# 计算损失值,使用平均平方误差
		loss = tf.losses.mean_squared_error(predictions, y)
		# 创建模型优化器并得到优化步骤
		train_op = tf.contrib.layers.optimize_loss(
			loss,
			tf.train.get_global_step(),
			optimizer=self.optimizer,
			learning_rate=self.learning_rate)
		return predictions, loss, train_op

	def fit(self,train_X=None,train_y=None):
		# 转化为LSTM模型的输入X
		train_X=train_X.reshape([-1,1,train_X.shape[1]])
		train_X=train_X.astype(np.float32)
		# 建立深层循环网络模型
		self.regressor = SKCompat(tf.contrib.learn.Estimator(model_fn=self.lstm_model))
		# 调用fit函数训练模型
		self.regressor.fit(train_X, train_y, batch_size=self.BATCH_SIZE, steps=self.TRAINING_STEPS)

	def predict(self,test_X):
		# 转化为LSTM模型的输入X
		test_X=test_X.reshape([-1,1,test_X.shape[1]])
		test_X=test_X.astype(np.float32)
		# 使用训练好的模型对测试集进行预测
		predicted = array([pred for pred in self.regressor.predict(test_X)])
		return predicted

class dp_CNN(object):

    def __init__(self, regularizer_weight=0.001):
        """
        创建一个卷积神经网络
        全连接中dropout的keepProb训练时在fit()传入,预测时在predict()中传入1.0
        """
        # 重置tensorflow的graph，确保神经网络可多次运行
        tf.reset_default_graph()
        tf.set_random_seed(1908)
        self.regularizer_weight = regularizer_weight
        self.W = []
        self.fnn_size=[5, 5, 1]

    def defineCNN(self,inputSize=None):
        """
        定义卷积神经网络的结构
        """
        img = tf.reshape(self.input, [-1, 1, inputSize, 1])
        # 定义卷积层1和池化层1，其中卷积层1里有4个feature map
        # convPool1的形状为[-1, 1, Xdim-3+1, 4] --> [-1, 1, (Xdim-3+1)/2, 4]
        convPool1 = self.defineConvPool(img, filterShape=[1, 3, 1, 4],
            poolSize=[1, 1, 2, 1])
        # 输出convPool1的维度信息
        # print(convPool1.get_shape().as_list())
        # 定义卷积层2和池化层2，其中卷积层2里有8个feature map
        # convPool2的形状为[-1, 4, 4, 40]
        convPool2 = self.defineConvPool(convPool1, filterShape=[1, 3, 4, 8],
            poolSize=[1, 1, 2, 1])
        # 输出convPool2的维度信息
        # print(convPool2.get_shape().as_list())
        # 将池化层2的输出变成行向量，后者将作为全连接层的输入
        pool_shape=convPool2.get_shape().as_list()
        convPool2 = tf.reshape(convPool2, [-1, pool_shape[1]*pool_shape[2]*pool_shape[3]])
        # 定义全连接层
        self.out = self.defineFullConnected(convPool2, size=self.fnn_size)

    def defineConvPool(self, inputLayer, filterShape, poolSize):
        """
        定义卷积层和池化层
        """
        weights = tf.Variable(tf.truncated_normal(filterShape, stddev=0.1))
        # 将模型中的权重项记录下来，用于之后的惩罚项
        self.W.append(weights)
        biases = tf.Variable(tf.zeros(filterShape[-1]))
        # 定义卷积层
        _conv2d = tf.nn.conv2d(inputLayer, weights, strides=[1, 1, 1, 1], padding="VALID")
        convOut = tf.nn.relu(_conv2d + biases)
        # 输出convOut的维度信息
        # print(convOut.get_shape().as_list())
        # 定义池化层
        poolOut = tf.nn.max_pool(convOut, ksize=poolSize, strides=poolSize, padding="SAME")
        return poolOut

    def defineFullConnected(self, inputLayer, size):
        """
        定义全连接层的结构
        """
        prevSize = inputLayer.shape[1].value
        prevOut = inputLayer
        layer = 1
        # 定义隐藏层
        for currentSize in size[:-1]:
            weights = tf.Variable(
                tf.truncated_normal([prevSize, currentSize], stddev=1.0 / np.sqrt(float(prevSize))),
                name="fc%s_weights" % layer)
            # 将模型中的权重项记录下来，用于之后的惩罚项
            self.W.append(weights)
            biases = tf.Variable(
                tf.zeros([currentSize]),
                name="fc%s_biases" % layer)
            layer += 1
            # 定义这一层神经元的输出
            neuralOut = tf.nn.relu(tf.matmul(prevOut, weights) + biases)
            # 对隐藏层里的神经元使用dropout
            prevOut = tf.nn.dropout(neuralOut, self.keepProb)
            prevSize = currentSize
        # 定义输出层
        weights = tf.Variable(tf.truncated_normal(
            [prevSize, size[-1]], stddev=1.0 / np.sqrt(float(prevSize))),
            name="output_weights")
        # 将模型中的权重项记录下来，用于之后的惩罚项
        self.W.append(weights)
        biases = tf.Variable(tf.zeros([size[-1]]), name="output_biases")
        out = tf.matmul(prevOut, weights) + biases
        return out

    def defineLoss(self):
        """
        定义神经网络的损失函数
        """
        # 定义单点损失，self.label是训练数据里的标签变量
        loss = tf.reduce_mean(tf.square(self.label - self.out))
        # L2惩罚项
        _norm = map(lambda x: tf.nn.l2_loss(x), self.W)
        regularization = reduce(lambda a, b: a + b, _norm)
        # 定义整体损失
        self.loss = tf.reduce_mean(loss + self.regularizer_weight * regularization,name="loss")
        # 记录训练的细节
        tf.summary.scalar("loss", self.loss)
        return self

    def SGD(self, X, Y, startLearningRate, miniBatchFraction, epoch, keepProb):
        """
        使用随机梯度下降法训练模型
        """
        trainStep = tf.Variable(0)
        learningRate = tf.train.exponential_decay(startLearningRate, trainStep,
            1000, 0.96, staircase=True)
        method = tf.train.GradientDescentOptimizer(learningRate)
        optimizer= method.minimize(self.loss, global_step=trainStep)
        batchSize = int(X.shape[0] * miniBatchFraction)
        batchNum = int(np.ceil(1 / miniBatchFraction)) 
        sess = tf.Session()
        self.sess = sess
        init = tf.global_variables_initializer()
        sess.run(init)
        step = 0
        while (step < epoch):
            for i in range(batchNum):
                batchX = X[i * batchSize: (i + 1) * batchSize]
                batchY = Y[i * batchSize: (i + 1) * batchSize]
                sess.run([optimizer], feed_dict={self.input: batchX, self.label: batchY, self.keepProb: keepProb})
            step += 1
        return self

    def fit(self, X=None, Y=None, startLearningRate=0.1, miniBatchFraction=0.1, epoch=3, keepProb=0.8):
        """
        训练模型
        """
        if len(Y.shape)==1:
            Y = Y.reshape([len(Y),1]) # 转成nx1数组,不会改变输入参数的值
        self.inputSize = X.shape[1]
        self.input = tf.placeholder(tf.float32, shape=[None, self.inputSize], name="X")
        self.label = tf.placeholder(tf.float32, shape=[None, 1], name="Y")
        self.keepProb = tf.placeholder(tf.float32)
        self.defineCNN(inputSize=self.inputSize)
        self.defineLoss()
        self.SGD(X, Y, startLearningRate, miniBatchFraction, epoch, keepProb)

    def predict(self, X):
        """
        使用神经网络对未知数据进行预测
        """
        sess = self.sess
        prob = sess.run(self.out, feed_dict={self.input: X, self.keepProb: 1.0})
        if len(prob.shape)==2:
            prob = prob.reshape([max(prob.shape),]) # 转成向量array,不会改变输入参数的值
        return prob


# 变量定义 -------------------------------------------------------------
deeplearning_methods={'LSTM':dp_LSTM,'CNN':dp_CNN}


