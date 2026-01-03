import psutil
import time
import sys

###################################################################
######## add prcoess names relevant to your machine below!!########
###################################################################

TARGET_PROCESSES: list[str] = ['MicrosoftEdgeUpdate.exe', 'GameBar.exe', 'msedgewebview2.exe', 'PhoneExperienceHost.exe', 'XboxPcAppFT.exe', 'GameBarPresenceWriter.exe', 'StoreDesktopExtension.exe']
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
#                                                                                                                                                                                                                                                                    
 ''')
print(f"microkiller started // task hitlist {TARGET_PROCESSES}")
print("press CTRL+C to stop")
####################################################################
CHECK_INTERVAL = 2 #### change seconds interval if you like ########
####################################################################

targets_lower: list[str] = [name.lower() for name in TARGET_PROCESSES]

try:
    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name and proc_name.lower() in targets_lower:
                    print(f"gotcha!! {proc_name} (PID: {proc.info['pid']}) // killing...")
                    proc.kill()
                    print(f"{proc_name} is dead\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception as e:
                print(f"err: {e}")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\nkilling spree concluded...")

    sys.exit(0)
