from effector_board import EffectorBoard
from effectors.distortion import Distortion
from parameters.distortion_parameters import DistortionParameters
from player import Player

FILENAME = "./test_data/guitar.wav"

def main():
    player = Player(FILENAME)
    distorion = Distortion()
    distorion.set_parameters(DistortionParameters(8))

    board = EffectorBoard([
        distorion
    ])
    board.print_effector_chain()
    player.set_effector_board(board)

    player.play()

if __name__ == "__main__":
    main()