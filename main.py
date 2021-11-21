import logging
import uvicorn

from core.api.app import app
from core.utils.utils import on_process_start


def main():
    on_process_start()

    port = 8000
    logging.info(f'Open http://localhost:{port}/ping')
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
