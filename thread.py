import threading
import subprocess


def executer_code_c(code):
    subprocess.run([code])


def executer_code_python():
    subprocess.run(["/usr/bin/python3", "multiplayer_connection.py"])


def worker(num):
    """Fonction exécutée par les threads."""
    print('Worker:', num)


# thread_python = threading.Thread(target=executer_code_python)
thread_c = threading.Thread(target=executer_code_c)
# thread_worker=threading.Thread(target=worker, args=(1,))

# Démarrage des threads

# thread_python.start()
thread_c.start()
# thread_worker.start()

# Attente de la fin des threads

# thread_python.join()
thread_c.join()
# thread_worker.join()

print("Fin du programme")
