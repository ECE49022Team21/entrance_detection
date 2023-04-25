from moms_apriltag import ApriltagBoard
import imageio

board = ApriltagBoard.create(1,1,"tag16h5", 10)
tgt = board.board

filename = "apriltag_target2.png"
imageio.imwrite(filename, tgt)

#from moms_apriltag import TagGenerator2
#from matplotlib import pyplot as plt

#tg = TagGenerator2("tag16h5")
#tag = tg.generate(1)

#filename = "apriltag_target1.png"
#imageio.imwrite(filename, tag)
