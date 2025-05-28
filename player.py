import numpy as np

from wave import Wave_read, open
from pyaudio import PyAudio
from threading import Thread
from enum import Enum
from effector_board import EffectorBoard
from exceptions import (
    AlreadyPlayingException,
    NotPlayingException,
    NotSetEffectorBoardException,
)
import globals

CHUNK = 256  # CHUNKフレームごとに再生


class Status(Enum):
    STOP = 0
    PLAY = 1
    PAUSE = 2


class Player:
    p = PyAudio()

    def __init__(
        self, wav_file: str, on_stop: callable = None, on_frame: callable = None
    ) -> None:
        self.wav_file: str = wav_file
        self.thread: Thread = None
        self.status: Status = Status.STOP
        self.w: Wave_read = open(self.wav_file, "rb")
        globals.CHANNELS = self.w.getnchannels()
        self.stream = None
        self.board: EffectorBoard = None
        self.__is_enable_effector_board: bool = False
        self.on_stop = on_stop
        self.on_frame = on_frame

    def set_effector_board(self, board: EffectorBoard) -> None:
        self.board = board
        self.__is_enable_effector_board = True

    def is_enable_effector_board(self) -> bool:
        return self.__is_enable_effector_board

    def enable_effector_board(self) -> None:
        if self.board is None:
            raise NotSetEffectorBoardException()

        self.__is_enable_effector_board = True

    def disable_effector_board(self) -> None:
        if self.board is None:
            raise NotSetEffectorBoardException()

        self.__is_enable_effector_board = False

    def __run(self):
        while self.status == Status.PLAY or self.status == Status.PAUSE:

            if self.status == Status.PAUSE:
                continue

            frames = self.w.readframes(CHUNK)

            # ==== 加工処理 ====
            data = np.frombuffer(frames, dtype=np.int16)

            if self.__is_enable_effector_board and self.board is not None:
                data = self.board.effect(data)
            # ==== 加工処理 ====

            if len(data) > 0:
                self.stream.write(data.tobytes())
            else:
                # 最後まで再生しきった場合
                self.status = Status.STOP
                self.stream.stop_stream()
                self.stream.close()
                self.w = open(self.wav_file, "rb")

                if self.on_stop is not None:
                    self.on_stop()

    def play(self) -> None:
        """
        再生を開始する。

        例外:
            AlreadyPlayingException: オーディオが既に再生中の場合に発生する。

        戻り値:
            なし
        """
        if self.status == Status.PLAY:
            raise AlreadyPlayingException()

        if self.status == Status.STOP:
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.w.getsampwidth()),
                channels=self.w.getnchannels(),
                rate=self.w.getframerate(),
                output=True,
            )
            self.thread = Thread(target=self.__run)
            self.status = Status.PLAY

            self.thread.start()
            return

        if self.status == Status.PAUSE:
            self.status = Status.PLAY

    def pause(self) -> None:
        """
        再生を一時停止する。

        例外:
            NotPlayingException: 状態がすでに一時停止／停止の場合に発生する。

        戻り値:
            なし
        """
        if self.status != Status.PLAY:
            raise NotPlayingException()

        self.status = Status.PAUSE

    def stop(self) -> None:
        """
        再生を停止する。

        例外:
            NotPlayingException: 状態がすでに一時停止／停止の場合に発生する。

        戻り値:
            なし
        """
        if self.status != Status.PLAY:
            raise NotPlayingException()

        self.status = Status.STOP
        self.w = open(self.wav_file, "rb")
        self.stream = None
        self.thread.join()

        if self.on_stop is not None:
            self.on_stop()
