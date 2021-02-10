from pydub import AudioSegment
from pydub.playback import play
import os


def get_audio_segment(audio_file_path: str = None, audio_file_name: str = None) -> AudioSegment:

    """
    Get an Audio Segment..
    :param audio_file_path: audio input file path
    :param audio_file_name: audio input file name; of type mp3, wav, mp4, ogg, wma, aac or flv
    :return: AudioSegment
    :exception: ValueError. if  audio input file path, and file name, not provided or is not off the supported format
    """

    # region guard condition(s)

    if audio_file_path is None or not os.path.isdir(audio_file_path):
        raise ValueError("Must provide an input file path")

    if audio_file_name is None or not os.path.isfile(audio_file_name):
        raise ValueError("Must provide an input file name; of type mp3, wav, mp4, ogg, wma, aac or flv")

    # endregion

    audio_file = os.path.join(audio_file_path, audio_file_name)

    return get_audio_segment(audio_file)


def get_audio_segment(audio_file: str = None) -> AudioSegment:
    """
        Get an Audio Segment..
        :param audio_file: audio input file; of type mp3, wav, mp4, ogg, wma, aac or flv
        :return: AudioSegment
        :exception: ValueError. if audio input file, not provided or is not off the supported format
        """

    # region guard condition(s)

    if audio_file is None or not os.path.isfile(audio_file):
        raise ValueError("Must provide an input file name; of type mp3, wav, mp4, ogg, wma, aac or flv")

    # endregion

    if audio_file.endswith('.mp3'):
        audio = AudioSegment.from_mp3(audio_file)
    elif audio_file.endswith('.wav'):
        audio = AudioSegment.from_wav(audio_file)
    elif audio_file.endswith('.ogg'):
        audio = AudioSegment.from_ogg(audio_file)
    elif audio_file.endswith('.flv'):
        audio = AudioSegment.from_flv(audio_file)
    else:
        try:
            extension = os.path.splitext(audio_file)
            audio = AudioSegment.from_file(audio_file, extension)
        except Exception:
            raise ValueError(f'audio_file = {audio_file} ; is not supported!')

    return audio


def play_audio_segment(from_audio_segment: AudioSegment = None) -> None:

    """
    Plays an audio segment
    :param from_audio_segment: to be played
    :return: None
    :exception: ValueError, if param is None
    """

    # region guard condition(s)
    if from_audio_segment is None:
        raise ValueError('Provided a Null/None, audio segment!')
    # endregion

    play(from_audio_segment)
