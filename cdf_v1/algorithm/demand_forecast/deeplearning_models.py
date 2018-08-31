#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-06-25 16:08:32
# @Author  : ${guoshengkang} (${kangguosheng1@huokeyi.com})

import os
import numpy as np
from numpy import *
import tensorflow as tf
from tensorflow.contrib.learn.python.learn.estimators.estimator import SKCompat

class dp_LSTM:
	"""
	Parameters
	------------
	Attributes
	------------
	"""
	def __init__(self,HIDDEN_SIZE=50,NUM_LAYERS=5,BATCH_SIZE=32,TRAINING_STEPS=3000,
		learning_rate=0.1,optimizer ='Adagrad'):
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
		# 建立深层循环网络模型
		self.regressor = SKCompat(tf.contrib.learn.Estimator(model_fn=self.lstm_model))
		# 调用fit函数训练模型
		self.regressor.fit(train_X, train_y, batch_size=self.BATCH_SIZE, steps=self.TRAINING_STEPS)

	def predict(self,test_X):
		# 使用训练好的模型对测试集进行预测
		predicted = array([pred for pred in self.regressor.predict(test_X)])
		return predicted

# 变量定义 -------------------------------------------------------------
deeplearning_methods={'LSTM':dp_LSTM}


