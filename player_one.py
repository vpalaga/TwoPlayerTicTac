from Player import Player

player = Player(is_host=True)
while True:
    player.pygame.update()
    mv = player.pygame.click()      # always read events, even on the opponent's turn
    if player.is_my_turn:
        if mv:
            player.play_move(mv)
    else:
        player.poll_opponent()