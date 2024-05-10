import psutil

def get_process_pid_by_name(process_name):
    for proc in psutil.process_iter():
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name'])
            if proc_info['name'] == process_name:
                return proc_info['pid'], proc_info['name']
        except psutil.NoSuchProcess:
            pass
    return None

print(get_process_pid_by_name('python'))
