from spotdl.authorize.services import AuthorizeSpotify
from spotdl import command_line

import logzero
import sys

def match_arguments(arguments):
    if arguments["song"]:
        for track in arguments["song"]:
            if track == "-":
                for line in sys.stdin:
                    command_line.helpers.download_track(
                        line,
                        arguments
                    )
            else:
                command_line.helpers.download_track(track, arguments)
    elif arguments["list"]:
        if arguments["write_m3u"]:
            youtube_tools.generate_m3u(
                track_file=arguments["list"]
            )
        else:
            list_download = {
                "sequential": command_line.helpers.download_tracks_from_file,
                "threaded"  : command_line.helpers.download_tracks_from_file_threaded,
            }[arguments["processor"]]

            list_download(
                arguments["list"],
                arguments,
            )
    elif arguments["playlist"]:
        spotify_tools.write_playlist(
            playlist_url=arguments["playlist"], text_file=arguments["write_to"]
        )
    elif arguments["album"]:
        spotify_tools.write_album(
            album_url=arguments["album"], text_file=arguments["write_to"]
        )
    elif arguments.all_albums:
        spotify_tools.write_all_albums_from_artist(
            artist_url=arguments["all_albums"], text_file=arguments["write_to"]
        )
    elif arguments.username:
        spotify_tools.write_user_playlist(
            username=arguments["username"], text_file=arguments["write_to"]
        )


def set_logger(level):
    fmt = "%(color)s%(levelname)s:%(end_color)s %(message)s"
    formatter = logzero.LogFormatter(fmt=fmt)
    logzero.formatter(formatter)
    logzero.loglevel(level)
    return logzero.logger


def main():
    arguments = command_line.get_arguments()
    logger = set_logger(arguments.log_level)
    logger.debug(arguments.__dict__)

    AuthorizeSpotify(
        client_id=arguments.spotify_client_id,
        client_secret=arguments.spotify_client_secret
    )
    # youtube_tools.set_api_key()

    try:
        match_arguments(arguments.__dict__)
    except KeyboardInterrupt as e:
        logger.exception(e)
        sys.exit(2)


if __name__ == "__main__":
    main()

