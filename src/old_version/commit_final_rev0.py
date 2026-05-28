"""
Programma che monitora la cartella C:\Work\marconilab
"""
import os
import time
from watchfiles import watch


def scrivi_log(evento, percorso_file):
    """Registra l'evento nel file log con timestamp.
    PEP8: Usiamo nomi di funzione minuscoli con underscore.
    """
    print("scrivi_log")
    orario = time.strftime("%Y-%m-%d %H:%M:%S")
    # Trasformiamo l'evento in stringa e lo puliamo un pò
    riga = f"{orario}; {str(evento)}\n"
    with open (percorso_file, mode="a", encoding="utf-8") as f_log:
        f_log.write(riga)
        print(riga)

        
def main():
    """Funzione che monitora la cartella del cliente
    """
    cartella_da_osservare = os.path.join("/work/marconilab")
    print(cartella_da_osservare)
    file_log = "..//log//commit_final.log"
    scrivi_log("log", file_log)
    print(f"--- commit_final attivo su {cartella_da_osservare} ---")
    print("Premi Ctrl + C per fermarlo se sei in console.")
                
if __name__ == "__main__":
    main()

