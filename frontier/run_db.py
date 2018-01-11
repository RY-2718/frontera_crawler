from frontera.worker.db import *
import signal

signal.signal(signal.SIGPIPE, signal.SIG_DFL)

parser = ArgumentParser(description="Frontera DB worker.")
parser.add_argument('--no-batches', action='store_true',
        help='Disables generation of new batches.')
parser.add_argument('--no-incoming', action='store_true',
        help='Disables spider log processing.')
parser.add_argument('--no-scoring', action='store_true',
        help='Disables scoring log processing.')
parser.add_argument('--config', type=str, required=True,
        help='Settings module name, should be accessible by import.')
parser.add_argument('--log-level', '-L', type=str, default='INFO',
        help="Log level, for ex. DEBUG, INFO, WARN, ERROR, FATAL.")
parser.add_argument('--port', type=int, help="Json Rpc service port to listen.")
args = parser.parse_args()

settings = Settings(module=args.config)
if args.port:
    settings.set("JSONRPC_PORT", [args.port])

logging_config_path = settings.get("LOGGING_CONFIG")
if logging_config_path and exists(logging_config_path):
    fileConfig(logging_config_path)
else:
    logging.basicConfig(level=args.log_level)
    logger.setLevel(args.log_level)
    logger.addHandler(CONSOLE)

worker = DBWorker(settings, args.no_batches, args.no_incoming, args.no_scoring)
server = WorkerJsonRpcService(worker, settings)
server.start_listening()
worker.run()
