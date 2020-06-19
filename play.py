import numpy as np
from skimage import io
import cv2
import random
from tensorflow.keras.models import load_model

def prepImg(pth):
    return cv2.resize(pth, (300, 300)).reshape(1, 300, 300, 3)


def updateScore(play, bplay, p, b):
    winRule = {'paper':'rock', 'rock':'lizard', 'lizard':'spock', 'spock':'scissors', 'scissors':'paper','paper':'spock', 'spock':'rock', 'rock':'scissors', 'scissors':'lizard', 'lizard':'paper'}
    if play == bplay:
        return p, b
    elif bplay == winRule[play]:
        return p + 1, b
    else:
        return p, b + 1


model="model_test .h5"
loaded_model=load_model(model)
print("Loaded model from disk")

shape_to_label = {'paper':np.array([1.,0.,0.,0.,0.]),'rock':np.array([0.,1.,0.,0.,0.]),'lizard':np.array([0.,0.,1.,0.,0.]),'spock':np.array([0.,0.,0.,1.,0.]),'scissors':np.array([0.,0.,0.,0.,1.])}
arr_to_shape= {np.argmax(shape_to_label[x]):x for x in shape_to_label.keys()}

options = ['paper', 'rock', 'lizard', 'spock', 'scissors']
winRule = {'paper':'rock', 'rock':'lizard', 'lizard':'spock', 'spock':'scissors', 'scissors':'paper','paper':'spock', 'spock':'rock', 'rock':'scissors', 'scissors':'lizard', 'lizard':'paper'}
rounds = 0
botScore = 0
playerScore = 0

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
loaded_model.predict(prepImg(frame[50:350, 100:400]))

NUM_ROUNDS = 3
bplay = ""

while True:
    ret, frame = cap.read()
    frame = frame = cv2.putText(frame, "Press Space to start", (160, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 0),
                                2, cv2.LINE_AA)
    cv2.imshow('Rock Paper Scissor lizard spock', frame)
    if cv2.waitKey(1) & 0xff == ord(' '):
        break

for rounds in range(NUM_ROUNDS):
    pred = ""
    for i in range(90):
        ret, frame = cap.read()

        # Countdown
        if i // 20 < 3:
            frame = cv2.putText(frame, str(i // 20 + 1), (320, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (250, 250, 0), 2,
                                cv2.LINE_AA)

        # Prediction
        elif i / 20 < 3.5:
            pred = arr_to_shape[np.argmax(loaded_model.predict(prepImg(frame[50:350, 100:400])))]

        # Get Bots Move
        elif i / 20 == 3.5:
            bplay = random.choice(options)
            print(pred, bplay)

        # Update Score
        elif i // 20 == 4:
            playerScore, botScore = updateScore(pred, bplay, playerScore, botScore)
            break

        cv2.rectangle(frame, (100, 150), (300, 350), (255, 255, 255), 2)
        frame = cv2.putText(frame, "Player : {}      Bot : {}".format(playerScore, botScore), (120, 400),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 0), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, pred, (150, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 0), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, "Bot Played : {}".format(bplay), (300, 140), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (250, 250, 0), 2, cv2.LINE_AA)
        cv2.imshow('Rock Paper Scissor lizard spock', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

if playerScore > botScore:
    winner = "You Won!!"
elif playerScore == botScore:
    winner = "Its a Tie"
else:
    winner = "Bot Won.."

while True:
    ret, frame = cap.read()
    frame = cv2.putText(frame, winner, (230, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 0), 2, cv2.LINE_AA)
    frame = cv2.putText(frame, "Press q to quit", (190, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 0), 2,
                        cv2.LINE_AA)
    frame = cv2.putText(frame, "Player : {}      Bot : {}".format(playerScore, botScore), (120, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 0), 2, cv2.LINE_AA)
    cv2.imshow('Rock Paper Scissor lizard spock', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()