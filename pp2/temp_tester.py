from Hex_KI import HexKI
import time



testKI = HexKI(4, 4)
testKI.player_colour = 1
testKI.opponent_colour = 2



# testKI.best_move = (0,0)
# testKI.nextMove()
# testKI.best_move = (1,0)
# testKI.nextMove()
#
# testKI.calculateMove()


# testKI.best_move = (0,2)
# testKI.nextMove()
# testKI.calculateMove()
#
# testKI.best_move = (0,3)
# testKI.nextMove()
for i in range(10):
    testKI.receiveMove(testKI.random_move())
    t0 = time.clock()
    testKI.calculateMove()
    print(time.clock() - t0)
    testKI.nextMove()




# for edge in testKI.edges:
#     print(edge)
# testKI.player_colour = 1
# print(testKI.evaluate())

print(testKI.evaluate())


testKI.opponent_colour = 2
move = (1, 1)
print("Make move {}".format(move))
testKI.receiveMove((move))

testKI.calculateMove()
testKI.nextMove()

print(testKI.evaluate())

testKI.opponent_colour = 1
move = (1, 2)
print("Make move {}".format(move))
testKI.receiveMove((move))

testKI.calculateMove()
testKI.nextMove()

testKI.player_colour = 1
testKI.opponent_colour = 2

print(testKI.evaluate())

