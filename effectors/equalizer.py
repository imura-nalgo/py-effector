from effectors.effector import Effector
import numpy as np
from scipy import signal as sg
from parameters.equalizer_parameters import EqualizerParameters
import globals


class PeakingFilter:
    def __init__(self):
        self.bw: float = None
        self.gain: float = None
        self.f: float = None
        self.sample_rate: float = None
        self.a: np.ndarray = None
        self.b: np.ndarray = None
        # フィルタ初期状態変数
        # チャンク間でフィルタ処理がリセットされるのを防ぐ。
        # チャンクごとに過渡応答が生じるのを防ぐことで、フィルタ処理を連続的にしたいみたい。
        self.zi = None

    def set_parameters(
        self,
        bw: float = 1.0,
        gain: float = 0.0,
        f: float = 0.0,
        sample_rate: float = 48000,
    ):
        self.bw = bw
        self.gain = gain
        self.f = f
        self.sample_rate = sample_rate

        self.b, self.a = self._calc_peaking_coefficients(
            self.bw, self.gain, self.f, self.sample_rate
        )

        # フィルタ係数の正規化
        # 特にa[0] = 1としておくことで、のちのフィルタ処理(lfilter)の計算量を減らす。
        self.b /= self.a[0]
        self.a /= self.a[0]

        # フィルタ初期状態計算
        self.zi = sg.lfilter_zi(self.b, self.a)

    def _calc_peaking_coefficients(
        self, bw: float, gain: float, f: float, sample_rate: float
    ) -> np.ndarray:
        # 計算式は以下を参照
        # https://www.utsbox.com/?page_id=523
        # bw: 帯域幅[octave]
        # gain: 音量[db]
        # f: 周波数[Hz]
        # sample_rate: サンプリングレート
        omega = 2.0 * np.pi * f / (sample_rate * globals.CHANNELS)
        alpha = np.sin(omega) * np.sinh(np.log(2.0) / 2.0 * bw * omega / np.sin(omega))
        A = 10 ** (gain / 40.0)

        a = np.array([1.0 + alpha / A, -2.0 * np.cos(omega), 1.0 - alpha / A])
        b = np.array([1.0 + alpha * A, -2.0 * np.cos(omega), 1.0 - alpha * A])

        return b, a

    def filter(self, input: np.ndarray[np.int16]) -> np.ndarray:
        output, self.zi = sg.lfilter(self.b, self.a, input, zi=self.zi)
        return output


class Equalizer(Effector):
    def __init__(self) -> None:
        self.name = "イコライザー"
        # イコライザーで調整できる周波数
        self.bands_hz = [200, 400, 800, 1600, 3200, 6400, 12800]
        self.filters_dict = dict()

        for b in self.bands_hz:
            f = PeakingFilter()
            f.set_parameters(
                1.0, 0, b, 48000  # TODO: wavファイルから取得できるように調整
            )
            self.filters_dict[b] = f

    def set_parameters(self, params: EqualizerParameters):
        self.filters_dict[params.hz].set_parameters(gain=params.gain, f=params.hz)

    def effect(self, input: np.ndarray) -> np.ndarray:
        np.set_printoptions(threshold=np.Inf)
        output = input

        for f in self.filters_dict.values():
            output = f.filter(output)

        return output.astype(np.int16)
