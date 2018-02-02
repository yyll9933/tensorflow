import tensorflow as tf
import numpy as np

# [털, 날개]
x_data = np.array(
    [[0, 0], [1, 0], [1, 1], [0, 0], [0, 0], [0, 1]])

# [기타, 포유류, 조류]
y_data = np.array([
    [1, 0, 0],  # 기타
    [0, 1, 0],  # 포유류
    [0, 0, 1],  # 조류
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 1]
])

## test set
#[털, 날개]
x_test = np.array(
    [[1, 0], [1, 0], [0, 1], [0, 0], [0, 0], [1, 0]])

# [기타, 포유류, 조류]
y_test = np.array([
    [0, 1, 0],  # 기타
    [0, 1, 0],  # 포유류
    [0, 0, 1],  # 조류
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 1]
])

X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)

# 첫번째 가중치의 차원은 [특성, 히든 레이어의 뉴런갯수] -> [2, 10] 으로 정합니다.
W1 = tf.Variable(tf.random_uniform([2, 10], -1., 1.))
# 두번째 가중치의 차원을 [첫번째 히든 레이어의 뉴런 갯수, 분류 갯수] -> [10, 3] 으로 정합니다.
W2 = tf.Variable(tf.random_uniform([10, 3], -1., 1.))

# 편향을 각각 각 레이어의 아웃풋 갯수로 설정합니다.
# b1 은 히든 레이어의 뉴런 갯수로, b2 는 최종 결과값 즉, 분류 갯수인 3으로 설정합니다.
b1 = tf.Variable(tf.zeros([10]))
b2 = tf.Variable(tf.zeros([3]))

# 신경망의 히든 레이어에 가중치 W1과 편향 b1을 적용합니다
L1 = tf.add(tf.matmul(X, W1), b1)
L1 = tf.nn.relu(L1)

# 최종적인 아웃풋을 계산합니다.
# 히든레이어에 두번째 가중치 W2와 편향 b2를 적용하여 3개의 출력값을 만들어냅니다.
model = tf.add(tf.matmul(L1, W2), b2)

# 텐서플로우에서 기본적으로 제공되는 크로스 엔트로피 함수를 이용해
# 복잡한 수식을 사용하지 않고도 최적화를 위한 비용 함수를 다음처럼 간단하게 적용할 수 있습니다.
cost = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=model))

optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
train_op = optimizer.minimize(cost)


#########
# 신경망 모델 학습
######
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

print("===X===")
print()
print(sess.run(X, feed_dict={X: x_data}))
print()

print("===Y===")
print()
print(sess.run(Y, feed_dict={Y: y_data}))
print()

print("===X*W1 + b1===")
print()
print(sess.run(tf.add(tf.matmul(X, W1), b1), feed_dict={X: x_data}))
print()

print("===Relu(X*W1 + b1)===")
print()
print(sess.run(L1, feed_dict={X: x_data}))
print()

print("===L1*W2 + b2===")
print()
print(sess.run(model, feed_dict={X: x_data}))
print()

print("===softmax_cross_entropy_with_logits===")
print()
print(sess.run(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=model), feed_dict={X: x_data, Y: y_data}))
print()

print("===cost = reduce_mean(softmax_cross_entropy_with_logits=)==")
print()
print(sess.run(tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=model)), feed_dict={X: x_data, Y: y_data}))
print()


for step in range(50):
    sess.run(train_op, feed_dict={X: x_data, Y: y_data})

    if (step + 1) % 20 == 0:
        print(step + 1, sess.run(cost, feed_dict={X: x_data, Y: y_data}))
        #print(sess.run(model, feed_dict={X: x_data, Y: y_data}))
        print()


#result
prediction = tf.argmax(model, 1)
target = tf.argmax(Y, 1)
print('예측값:', sess.run(prediction, feed_dict={X: x_test}))
print('실제값:', sess.run(target, feed_dict={Y: y_test}))

is_correct = tf.equal(prediction, target)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print('정확도: %.2f' % sess.run(accuracy * 100, feed_dict={X: x_data, Y: y_data}))
