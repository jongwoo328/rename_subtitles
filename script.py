import glob
import os
import sys
import traceback
from datetime import datetime

class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
VIDEO_EXT = None
SUBTITLE_EXT = None
ERR_LOG_FILE = 'error_log.txt'
VERSION = '1.0.0'

def get_files(file_list, ext):
    result = []
    for f in file_list:
        extension = f.split('.')[-1]
        if extension == ext:
            result.append(f)
    return result

def sort_by_number(x):
    return int(''.join(filter(str.isdigit, x)))

print(f'\n스크립트를 시작합니다. {bcolors.WARNING}ver {VERSION}{bcolors.ENDC}\n')
while VIDEO_EXT is None or SUBTITLE_EXT is None:
    VIDEO_EXT = input('동영상의 확장자를 입력하세요 ex) mp4 : ')
    SUBTITLE_EXT = input('자막의 확장자를 입력하세요 ex) smi : ')

file_list = os.listdir(BASE_DIR)

video_files = sorted(get_files(file_list, VIDEO_EXT), key=sort_by_number)
subtitle_files = sorted(get_files(file_list, SUBTITLE_EXT), key=sort_by_number)

if len(video_files) != len(subtitle_files):
    print(f'\n{bcolors.WARNING}{bcolors.OKCYAN}{VIDEO_EXT}{bcolors.ENDC} 파일의 수와 {bcolors.OKCYAN}{SUBTITLE_EXT}{bcolors.ENDC} 파일의 수가 맞지 않습니다.{bcolors.ENDC}')
    exit()
else:
    print(f'\n영상 파일 : {VIDEO_EXT}  ({len(video_files)} 개)')
    print(f'자막 파일 : {SUBTITLE_EXT}  ({len(subtitle_files)} 개)\n')

    for idx, video_file in enumerate(video_files):
        video_file_name = video_file.split(f'.{VIDEO_EXT}')[0]

        old_subtitle_file = os.path.join(BASE_DIR, subtitle_files[idx])

        new_file = f'{video_file_name}.{SUBTITLE_EXT}'
        new_subtitle_file = os.path.join(BASE_DIR, f'{new_file}')
        
        try:
            message = f'변경 : {subtitle_files[idx]}  =>  {new_file}'
            print(message)
            os.rename(old_subtitle_file, new_subtitle_file)
            sys.stdout.write("\033[F")
            print(message + f' ---- {bcolors.OKBLUE}SUCCESS{bcolors.ENDC}')
        except Exception as err:
            sys.stdout.write("\033[F")
            print(message + f' ---- {bcolors.FAIL}FAIL{bcolors.ENDC}')

            error_log = f'[ {datetime.now()} ]\n{traceback.format_exc()}'
            with open(os.path.join(BASE_DIR, ERR_LOG_FILE), 'w') as log:
                log.write(error_log)
            print(f'{bcolors.FAIL}\n에러로 인해 작업이 완료되지 않았습니다.{bcolors.ENDC}')
            print(f'{bcolors.FAIL}{ERR_LOG_FILE} 파일을 확인해주세요.{bcolors.ENDC}')
            exit()
    else:
        print(f'\n{bcolors.WARNING}변환이 완료되었습니다.{bcolors.ENDC}\n')
    
