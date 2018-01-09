from gi.repository import GLib

import app


if __name__ == '__main__':
    app.logger.info('Running main loop')
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        app.logger.info("Loop stopped")