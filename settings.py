class Settings:
    """ Window Settings """
    window_title              = "RockFall"
    window_bg_color           = "gray"
    window_height             = 700
    window_width              = 600

    """ Player Settings """
    player_tag                = "player"
    player_color              = "#ff0000"
    player_ghost_color        = "#ffe6e6"
    player_ghost_dur          = 2000          # ms
    player_height             = 50
    player_width              = 50
    player_velocity           = 50
    player_lives              = 3

    """ Rock Settings """
    rock_color                = "black"
    rock_tag                  = "rock"
    rock_height               = 50
    rock_width                = 50
    rock_fall_velocity        = 15
    rock_miss_score           = 10
    rock_spawn_interval       = 500

    """ General Bonus Settings """
    bonus_color               = "blue"
    bonus_tag                 = "bonus"
    bonus_height              = 50
    bonus_width               = 50
    bonus_fall_velocity       = 15
    bonus_spawn_rate_min      = 5000
    bonus_spawn_rate_max      = 10000

    """ Speed Bonus Settings """
    bonus_insanity_game_delay = 10
    bonus_insanity_spawn_rate = 250
    bonus_insanity_score_mult = 10
    bonus_insanity_duration   = 4000

    """ Game Settings """
    game_delay                = 20
    game_score_multiplier     = 1
