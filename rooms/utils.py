from django.core.signing import Signer
import random
def generate_room_code(room_id):
    str_room_id = str(room_id)
    print('str_room_id: ', str_room_id)

    # generate room code
    # by signing on room_id with user id salt
    signer = Signer()

    # if room id is 5
    # generated code will be '5:<string of size 43>'
    # exclude '5:'
    room_code = signer.sign(str_room_id)[(len(str_room_id) + 1):]
    print('room_code: ', room_code)


def generate_room_code_new(room_id):
    s = 'abcdefghijklmnopqrstuvwxyz'
    def r(): 
        return random.randint(0,25)
    # print('str_room_id: ', str_room_id)

    # generate room code

    # if room id is 5
    # generated code will be '5:<string of size 43>'
    # exclude '5:'
    room_code = f'{s[r()]}{s[r()]}{s[r()]}-{s[r()]}{s[r()]}{s[r()]}{s[r()]}-{s[r()]}{s[r()]}{s[r()]}'

    return room_code
