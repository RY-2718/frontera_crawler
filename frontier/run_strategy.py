from frontera.worker.strategy import *
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

settings, strategy_class = setup_environment()
worker = StrategyWorker(settings, strategy_class)

worker.run()
