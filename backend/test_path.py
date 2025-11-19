import platform

def win_to_wsl_path(win_path):
    wsl_path = win_path.replace('\\\\', '/')
    if ':' in wsl_path:
        drive = wsl_path[0].lower()
        rest = wsl_path[2:]
        wsl_path = f'/mnt/{drive}{rest}'
    return wsl_path

test_path = 'C:/Users/user/AppData/Local/Temp/test/playbook.yml'
print(f'Windows: {test_path}')
print(f'WSL: {win_to_wsl_path(test_path)}')

test_path2 = 'C:\\\\Users\\\\user\\\\AppData\\\\Local\\\\Temp\\\\test\\\\playbook.yml'
print(f'Windows2: {test_path2}')
print(f'WSL2: {win_to_wsl_path(test_path2)}')
