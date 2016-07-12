from Hex_KI import HexKI

testKI = HexKI(4, 4)
testKI.player_colour = 1
testKI.opponent_colour = 2


for i in range(10):
    testKI.receiveMove(testKI.random_move())
    testKI.calculateMove()
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

