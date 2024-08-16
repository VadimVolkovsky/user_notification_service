from handlers.events import broker
from faststream import FastStream

app = FastStream(broker)
