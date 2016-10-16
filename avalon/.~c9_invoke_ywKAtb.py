def send_to_que

def last_sender(the_)

def send_to_queue( player, content ):
    if len(player.text_queue) == 0:
        threading.Thread( target = last_sender, args=(player.id, context ) )
    else:
        player.text_queue.push[ context ]