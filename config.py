class Config:
    music_on = True
    sfx_on = True
    hard_mode = False

    @staticmethod
    def get_pipe_speed(score):
        # Base speed increases by 1 for every 5 points. Max speed is 10.
        base_speed = 6 if Config.hard_mode else 4
        speed_boost = score // 5
        return min(base_speed + speed_boost, 10)

    @staticmethod
    def get_pipe_frequency(score):
        # Pipes spawn 100ms faster for every 5 points. Fastest is 900ms.
        base_freq = 1200 if Config.hard_mode else 1500
        freq_boost = (score // 5) * 100
        return max(base_freq - freq_boost, 900)