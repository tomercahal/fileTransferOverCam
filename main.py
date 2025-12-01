import sys
from receiver import receiver_main
from sender import sender_main

def main():
    mode = sys.argv[1]
    if mode == 'sender':
        print('Starting sender mode...')
        sender_main()
    elif mode == 'receiver':
        print('Starting receiver mode...')
        receiver_main()
    else:
        print("Invalid mode. Use 'sender' or 'receiver'.")

if __name__ == '__main__':
    main()
