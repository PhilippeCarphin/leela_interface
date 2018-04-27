Note, this has turned out to be more general than being just an interface to leela.

This is actually a higher level wrapper around a subprocess.  It's a wrapper around
a process created subprocess.Popen() that provides two queues that are filled in
asynchronously from the stdout and stderr of the process.

The method names still have leela_this and leela_that and I have to change that.

A propos des subprocess et pipe Unix
====================================

Si on ne sait pas c'est quoi un pipe Unix, ou les I/O streams : stdout, stdin, stderr:

Les programmes ont des "channel" de input ou de output.  Le channel stdin est un "channel" de input.  Les "channels" stdout et stderr sont des channels de output.

Chaque process les a.  Normalement stdin est branché sur notre terminal, de sorte que le programme peut faire des getchar() ou readline(). Ensuite stdout et stderr sont aussi normalement branchés sur notre terminal de sorte que quand on fait des prints(), ça sort dans notre termina.

Les "pipe" servent à relier ces choses ensemble.  Au lieu que le input qui arrive sur stdin vienne du terminal, il peut venir d'un autre processus qui va écrire sur ce pipe.  Au lieu que le output aille au terminal, il peut aller à un autre processus qui fera des lectures sur ce pipe.


En Python : subprocess.Popen
============================

En python, on peut créer un processus avec

	my_process_object = subprocess.Popen(<commande>, <autres_arguments>).  

Ceci crée un processus qui exécute <commande>.  Les <autres_arguments> permettent de décider si on veut des pipes connectés aux différent "channels" de ce processus.

La fonction retourne un opjet qui aura des attributs my_process_object.{stdin, stdout, stderr} qui sont des objets IOTextWrapper qui offrent, entre autres, les méthodes write(bytes) et readline().


Cas particulier : leela-zero
============================

Dans le cas de mon interaction avec leela
Quand je crée le process leela, je fais des pipes.

	engine_cmd = ['leelaz', '-g', '-w', './src/leelaz-model-530930-128000.txt']

    self._leela_process = subprocess.Popen(
            engine_cmd,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

Leela écoute sur stdin pour ses commandes.  Donc je lui écris des commandes en faisant self._leela_process.stdin.write(...).

Ensuite j'ai deux autres pipes sur lesquels j'écoute.  Un qui pluggé sur le stdout de leela, leela écrit là dessus sa réponse finale.  Un autre qui est pluggé sur le stderr de leela.  Sur celui là, leela écrit son analyse et d'autres infos.

Le code est ultra simple, mais ça m'a pris beaucoup d'expérimentation pour comprendre comment faire les pipe et écouter dessus sans bloquer.

Écouter sur un pipe sans bloquer
================================

Je dois faire des self._leela_process.stderr.readline().

Sauf que c'est bloquant, tant qu'il a pas consommé une ligne de sur le pipe, on bloque sur le read.

Si on sait combien de lignes le output va avoir c'est pas un problème, on fait le nombre correspondant de readline(), mais si on sait pas, c'est un petit casse-tête.

C'est un problème commun et la solution c'est de faire un thread qui écoute sur stderr et accumule ce qu'il lit dans une queue multithread de lignes.

Quand on se fait informer par nos self._leela_process.stdout.readline() que leela a fini de servir la commande, on prend toutes les lignes de cette queue (on la vide).  Et on sait que c'est ça le output sur stderr pour le coup en question.
