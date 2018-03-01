import pexpect

cmd = 'python3.5 /home/pi/Pizik/modules/sequenceur/piano_graphique.py'

child = pexpect.spawn(cmd)
while True:
    try:
        child.expect('test')
        print(child.after)
    except pexpect.EOF:
        break 
