from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import audio_player
import requests
import pprint

URL = os.environ.get('IBM_WATSON_BASE_URL')
VOICE_URL = os.path.join(URL, os.environ.get('IBM_WATSON_VOICES_BASE_URL'))

API_KEY = os.environ.get('IBM_WATSON_API_KEY')

TEMP_DIR = os.environ.get('IBM_WATSON_TEMP_AUDIO_DIR')
TEMP_AUDIO_FILE = os.environ.get('IBM_WATSON_TEMP_AUDIO_FILE')


class VoiceResponseError(ValueError):
    pass


def say(phrase: str = None, voice: str = None, save_file: bool = False,
        save_file_to_path: str = TEMP_DIR, file_name: str = TEMP_AUDIO_FILE) -> None:
    """
        SPEAK using IBM Watson TTS
        @raise ValueError, if a @param phrase; is not provided, and default to None
    """

    # region guard condition(s)

    if phrase is None:
        raise ValueError("Must provide a phrase to speak")

    if save_file:

        if save_file_to_path is None or not os.path.isdir(save_file_to_path):
            raise ValueError("Must provide an output file path")

        if file_name is None:
            raise ValueError("Must provide an output file of type mp3")

    # endregion

    print(voice)

    authenticator = IAMAuthenticator(f'{API_KEY}')

    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(f'{URL}')

    response = text_to_speech.synthesize(
        f'{phrase}',
        voice='en-US_AllisonV3Voice' if voice is None else voice,
        accept='audio/mp3'
    ).get_result()

    destination = os.path.join(save_file_to_path, file_name)

    if not save_file:
        os.makedirs(save_file_to_path, exist_ok=True)

    with open(destination, 'wb') as audio_file:
        audio_file.write(response.content)

    audio_segment = audio_player.get_audio_segment(destination)

    audio_player.play_audio_segment(audio_segment)


def query_voices() -> list:
    with requests.get(url=VOICE_URL, auth=('apikey', API_KEY)) as response:
        if response.status_code not in range(200, 300):
            raise VoiceResponseError('Could not get Voices, from IBM Watson!')
        response_json = response.json()

    voices: list = response_json.get('voices')
    return voices


def get_languages() -> list:
    return [
        'Arabic',
        'German',
        'English',
        'Spanish',
        'French',
        'Italian',
        'Japanese',
        'Korean',
        'Dutch',
        'Portuguese',
        'Chinese',
    ]


def get_language_abbreviations() -> list:
    return [
        'ar',
        'de',
        'en',
        'es',
        'fr',
        'it',
        'ja',
        'ko',
        'nl',
        'pt',
        'zh',
    ]


def get_voice_types() -> list:
    return ["Enhanced", "Neural"]


def get_voice_type_abbreviations() -> list:
    return ["V3", "Voice"]


def lookup_gender_voices(voices: list = None, gender: str = 'male') -> list:
    # region guard condition for voices
    if voices is None or len(voices) == 0:
        raise VoiceResponseError('Provided invalid voices')

    #  endregion guard condition for voices

    def filter_voices_by_gender() -> list:
        attribute: str = 'gender'
        matched_lookup_voices: list = []
        for voice_data in voices:
            voice: dict = voice_data
            if not (voice.get(attribute) == gender):
                continue
            matched_lookup_voices.append(voice)
        return matched_lookup_voices

    return filter_voices_by_gender()


def lookup_language_voices(gender_voices: list = None, language_abbreviation: str = 'en') -> list:
    # region guard condition for gender_voices
    if gender_voices is None or len(gender_voices) == 0:
        raise VoiceResponseError(gender_voices, "Provider invalid gender_voices!")

    #  endregion guard condition for gender_voices

    def filter_voices_by_language():
        attribute: str = 'language'
        matched_lookup_voices: list = []
        for voice_data in gender_voices:
            voice: dict = voice_data
            voice_language: str = voice.get(attribute)
            if not (voice_language.find(language_abbreviation) > -1):
                continue
            matched_lookup_voices.append(voice)
        return matched_lookup_voices

    return filter_voices_by_language()


def lookup_voice_types(gender_voices: list = None, voice_type: str = "Enhanced") -> list:
    # region guard condition for gender_voices
    if gender_voices is None or len(gender_voices) == 0:
        raise VoiceResponseError("Provider invalid gender_voices!")

    #  endregion guard condition for gender_voices

    def filter_voices_by_type():

        attribute: str = 'name'

        matched_lookup_voices: list = []

        enhanced_type = get_voice_types()[0]
        enhanced_type_abbreviation = get_voice_type_abbreviations()[0]

        neural_type = get_voice_types()[1]
        neural_type_abbreviation = get_voice_type_abbreviations()[1]

        for voice_data in gender_voices:

            voice: dict = voice_data
            voice_type_abbreviate: str = enhanced_type_abbreviation if voice_type == enhanced_type else neural_type_abbreviation
            voice_attribute = voice.get(attribute)

            if voice_type == enhanced_type and voice_type_abbreviate == enhanced_type_abbreviation:
                if not (voice_attribute.find(enhanced_type_abbreviation) > -1):
                    continue
            elif voice_type == neural_type and voice_type_abbreviate == neural_type_abbreviation:
                if not (voice_attribute.find(neural_type_abbreviation) > -1):
                    continue

            matched_lookup_voices.append(voice)

        return matched_lookup_voices

    return filter_voices_by_type()


def lookup_enhanced_voice_types(gender_voices: list = None) -> list:
    # region guard condition for gender_voices
    if gender_voices is None or len(gender_voices) == 0:
        raise VoiceResponseError("Provider invalid gender_voices!")

    #  endregion guard condition for gender_voices

    return lookup_voice_types(
        gender_voices=gender_voices,
        voice_type=get_voice_types()[0]
    )


def lookup_neural_voice_types(gender_voices: list = None) -> list:
    # region guard condition for gender_voices
    if gender_voices is None or len(gender_voices) == 0:
        raise VoiceResponseError("Provider invalid gender_voices!")

    #  endregion guard condition for gender_voices

    return lookup_voice_types(
        gender_voices=gender_voices,
        voice_type=get_voice_types()[1]
    )


def get_sorted_voices(voice_attribute: dict = None) -> list:
    # region guard condition for voice_attribute: dict
    if voice_attribute is None or voice_attribute == {}:
        raise ValueError('voice_attribute: dict is either empty or None, and this invalid!')
    # endregion guard condition for voice_attribute: dict

    enhanced_voices = voice_attribute.get('type').get('enhanced_voices')

    voice_list = []

    for index, language in enumerate(voice_attribute.get('language_attribute').get("languages")):
        voice_languages = lookup_language_voices(
            gender_voices=voice_attribute.get('voices'),
            language_abbreviation=voice_attribute.get('language_attribute').get(
                "language_abbreviations")[index])
        for voice_type in get_voice_types():
            for voice_data in voice_languages:
                voice: dict = voice_data
                is_voice_enhanced = voice in enhanced_voices

                if not (voice_type == (get_voice_types()[0] if is_voice_enhanced else get_voice_types()[1])):
                    continue

                voice_list.append({
                    'Name': voice.get("name"),
                    'Gender': voice.get("gender"),
                    'Language': voice.get("language"),
                    'Type': voice_type,
                    'Description': voice.get("description")
                })

    return voice_list


def get_language_attribute():
    return {
        'languages': get_languages(),
        'language_abbreviations': get_language_abbreviations()
    }


def get_voice_attribute(gender_voices=None):
    # region guard condition for gender_voices
    if gender_voices is None or gender_voices == []:
        raise ValueError('invalid gender_voices!')
    # endregion guard condition for gender_voices

    return {
        "voices": gender_voices,
        'language_attribute': get_language_attribute(),
        "type": {"enhanced_voices": lookup_enhanced_voice_types(gender_voices)}
    }


class IBMVoices(object):

    def __init__(self):
        self.ibm_voices = query_voices()
        self.ibm_male_voices = lookup_gender_voices(voices=self.get_voices(), gender='male')
        self.ibm_female_voices = lookup_gender_voices(voices=self.get_voices(), gender='female')
        self.ibm_sorted_male_voices = get_sorted_voices(voice_attribute=get_voice_attribute(gender_voices=self.get_male_voices()))
        self.ibm_sorted_female_voices = get_sorted_voices(voice_attribute=get_voice_attribute(gender_voices=self.get_female_voices()))
        pass

    def get_voices(self) -> list:
        return self.ibm_voices

    def get_male_voices(self) -> list:
        return self.ibm_male_voices

    def get_female_voices(self) -> list:
        return self.ibm_female_voices

    def get_all_male_voices_sorted(self) -> list:
        return self.ibm_sorted_male_voices

    def get_all_female_voices_sorted(self) -> list:
        return self.ibm_sorted_female_voices


try:
    ibm_voice_instance = IBMVoices()
except Exception:
    # todo test offline, and on trail subscription ended!
    pass


def get_voice_instance():
    return ibm_voice_instance
