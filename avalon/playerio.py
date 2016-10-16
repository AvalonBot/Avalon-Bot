import threading
import urllib3

urllib3.disable_warnings()
http = urllib3.PoolManager()

def last_sender(player):
    content = player.text_deque[0]

    res = http.request( content[0], content[1], body=content[2], headers=content[3] )
    check(res)
    player.text_lock.acquire()
    player.text_deque.popleft()
    player.text_lock.release()
    
    if len( player.text_deque ) > 0:
        last_sender( player )

# Main function to send message to player
def send_to_queue( player, content ):
    if len(player.text_deque) == 0:
        player.text_deque.append( content )
        
        t = threading.Thread( target = last_sender, args=(player,) )
        t.start()
    else:
        player.text_lock.acquire()
        player.text_deque.append( content )
        player.text_lock.release()
    return True
        
# check the response status
def check(res):
    if res.status == 200:
        return True
    else:
        print( res.status )
        print( 'res = ' + str( res.data ) )
        return False