import os
import time

emulation_config = "/home/tipi/.emulation"


def status():
    enabled = os.path.exists(emulation_config)
    nfs = False
    pdf = True
    if enabled:
        with open(emulation_config, "r") as f:
            lines = f.readlines()
            pdf = "PDF_ENABLED=1\n" in lines
            nfs = "NFS_ENABLED=1\n" in lines
        
    return {
        "enabled": enabled,
        "nfs": nfs,
        "pdf": pdf
    }


def update(state):
    if not state['enabled']:
        os.remove(emulation_config)
        restart()
    else:
        nfs = 1 if state['nfs'] else 0
        pdf = 1 if state['pdf'] else 0
        with open(emulation_config, "w") as f:
            f.write(f"NFS_ENABLED={nfs}\n")
            f.write(f"PDF_ENABLED={pdf}\n")
        restart()
    

def restart():
    with open("/tmp/tipi_restart", "w") as f:
        f.write("restart services")
    while os.path.exists("/tmp/tipi_restart"):
        time.sleep(3)

