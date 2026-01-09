import psutil
import time
import sys
import os

###################################################################
######## add prcoess names relevant to your machine below!!########
###################################################################
TARGET_PROCESSES: list[str] = ['UserOOBEBroker.exe', 'OneDrive.Sync.Service.exe', 'MicrosoftEdgeUpdate.exe', 'GameBar.exe', 'msedgewebview2.exe', 'PhoneExperienceHost.exe', 'XboxPcAppFT.exe', 'GameBarPresenceWriter.exe', 'StoreDesktopExtension.exe']
###################################################################
CHECK_INTERVAL = 2 #### change seconds interval if you like ########
####################################################################
HIT_COUNT = int(len(TARGET_PROCESSES))
BODY_COUNT = int(0)

try:
    import pynvml
    HAS_NVML = True
    pynvml.nvmlInit()
except ImportError:
    HAS_NVML = False
    print("nvidia-ml-py not installed – GPU monitoring disabled.")
except pynvml.NVMLError:
    HAS_NVML = False
    print("No NVIDIA GPU detected or driver issue – GPU monitoring disabled.")

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)  # Accurate over 1 second

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used / (1024**3), mem.total / (1024**3)  # % , used GB, total GB

def get_gpu_usage():
    if not HAS_NVML:
        return "N/A (no NVIDIA GPU or library)"
    
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count == 0:
            return "No GPU detected"
        
        info_lines = []
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            
            gpu_util_pct = util.gpu
            mem_util_pct = util.memory
            mem_used_gb = mem_info.used / (1024**3)
            mem_total_gb = mem_info.total / (1024**3)
            
            info_lines.append(
                f"{name}\033[92m / \033[0mutil: {gpu_util_pct}%\033[92m / \033[0mmem: {mem_util_pct}% "
                f"[{mem_used_gb:.1f}/{mem_total_gb:.1f} gb]"
            )
        return " | ".join(info_lines)
    except pynvml.NVMLError as e:
        return f"GPU error: {e}"

###################################################################
######################### l33t banner #############################
###################################################################
print('''
#
#
#    ███    ███ ██  ██████ ██████   ██████  ██   ██ ██ ██      ██      ███████ ██████  
#    ████  ████ ██ ██      ██   ██ ██    ██ ██  ██  ██ ██      ██      ██      ██   ██ 
#    ██ ████ ██ ██ ██      ██████  ██    ██ █████   ██ ██      ██      █████   ██████  
#    ██  ██  ██ ██ ██      ██   ██ ██    ██ ██  ██  ██ ██      ██      ██      ██   ██ 
#    ██      ██ ██  ██████ ██   ██  ██████  ██   ██ ██ ███████ ███████ ███████ ██   ██ 
#                                                                                      
#''')
print(f"# microkiller [\033[92mstarted\033[0m] \033[92m//\033[0m [\033[91m{HIT_COUNT}\033[0m] tasks in hitlist \033[92m//\033[0m \033[90mpress CTRL+C to\033[0m\033[91m kill\033[0m")

targets_lower: list[str] = [name.lower() for name in TARGET_PROCESSES]

try:
    while True:
        
        cpu_pct = get_cpu_usage()
        ram_pct, ram_used_gb, ram_total_gb = get_ram_usage()
        gpu_info = get_gpu_usage()
    
        # Clear line and print updated status (overwrites previous line)
        sys.stdout.write('\r' + ' ' * 100 + '\r')  # Clear previous line
        sys.stdout.write(
            f"# cpu:{cpu_pct:5.1f}%\033[92m / \033[0m"
            f"ram:{ram_pct:5.1f}% [{ram_used_gb:.1f}/{ram_total_gb:.1f} gb]\033[92m / \033[0m"
            f"{gpu_info}"
            f"\033[92m / \033[0mkills [\033[91m{BODY_COUNT}\033[0m]"
        )
        sys.stdout.flush()
    
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                
                proc_name = proc.info['name']
                if proc_name and proc_name.lower() in targets_lower:
                    proc.kill()
                    BODY_COUNT = BODY_COUNT + 1
                    sys.stdout.write('\r' + ' ' * 100 + '\r')
                    sys.stdout.write(
                        f"\n# killed process [\033[91m{proc_name}\033[0m] \033[90m(PID: {proc.info['pid']})\033[0m"
                    )
                    sys.stdout.flush()
  
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception as e:
                print(f"# err:\033[91m {e}\033[0m")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print(f"\n# killing spree [\033[92mconcluded\033[0m] \033[92m//\033[0m body count [\033[91m{BODY_COUNT}\033[0m]")
    sys.exit(0)


