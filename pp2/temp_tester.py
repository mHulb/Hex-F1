from Hex_KI import HexKI

testKI = HexKI(3, 3)
for edge in testKI.edges:
    print(edge)

testKI.opponent_colour = 1
move = (1, 1)
print("Make move {}".format(move))
testKI.receiveMove((move))

for edge in testKI.edges:
    print(edge)


testKI.opponent_colour = 2
move = (1, 2)
print("Make move {}".format(move))
testKI.receiveMove((move))

for edge in testKI.edges:
    print(edge)


