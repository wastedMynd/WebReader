import eel
from natural_tts import say, get_voice_instance, get_language_attribute
from jinja2 import Environment, FileSystemLoader
import os
import audio_player

project_folder = '/home/sizwe/PycharmProjects/WebReader'
temp_audio_folder = os.path.join(project_folder, 'temp_watson_audio')
web_folder = os.path.join(project_folder, 'web')
templates_folder = os.path.join(web_folder, 'templates')

eel.init('web', allowed_extensions=['.js', '.html'])


class EmptyTextError(ValueError):
    pass


def render():

    # region guard for ibm_voices
    if get_voice_instance() is None:
        raise ValueError(
            get_voice_instance(),
            'ibm_voices, can not be obtained, this may due to bad connection, or service no longer available!'
        )
    #  endregion guard for ibm_voices


    loader = FileSystemLoader(templates_folder)
    env = Environment(loader=loader)
    env.globals['enumerate'] = enumerate
    template = env.get_template('main_temp.html')

    page_to_render = os.path.join(web_folder, 'main.html')

    def get_gender_voices(ibm_voices_for_gender):
        lang_dic = {}
        lang_lis = []

        for lang in get_language_attribute().get('language_abbreviations'):
            for voice in ibm_voices_for_gender:
                if voice.get('Language').find(lang) > -1:
                    lang_lis.append(voice)
            lang_dic.update({lang: lang_lis})
            lang_lis = []

        return lang_dic

    def get_voice_type_heading(previous_voice, voice):
        voice_type_heading = ""

        current_person = (
            voice.get('Name')
            .replace(voice.get('Language') + '_', '')
            .replace('V3Voice', ' Natural')
            .replace('V2Voice', ' Artificial')
            .replace('Voice', ' Computerized')
        )
        current_person_data = current_person.split(' ')
        current_person_voice_type = current_person_data[1]

        if previous_voice is None:
            voice_type_heading = f'<optgroup class="voice_type" label="{current_person_voice_type + " Voice"}">'
        else:
            previous_person = (
                previous_voice.get('Name')
                    .replace(voice.get('Language') + '_', '')
                    .replace('V3Voice', ' Natural')
                    .replace('V2Voice', ' Artificial')
                    .replace('Voice', ' Computerized')
            )
            previous_person_data = previous_person.split(' ')
            previous_person_voice_type = previous_person_data[1]

            if previous_person_voice_type != current_person_voice_type:
                voice_type_heading = '</optgroup>\n'
                voice_type_heading += f'<optgroup class="voice_type" label="{current_person_voice_type + " Voice"}">'

        return voice_type_heading

    def apply_closing_voice_type_heading_tag(vx, voices):
        if vx == len(voices) - 1:
            return '</optgroup>'
        else:
            return ''


    with open(page_to_render, 'w') as page_to_render_writer:
        page_to_render_writer.write(template.render(
            lang=get_language_attribute(),
            male_voices=get_gender_voices(get_voice_instance().get_all_male_voices_sorted()),
            female_voices=get_gender_voices(get_voice_instance().get_all_female_voices_sorted()),
            get_voice_type_heading=get_voice_type_heading,
            apply_closing_voice_type_heading_tag=apply_closing_voice_type_heading_tag,
            get_watson_display_voice=get_watson_display_voice
        ))

    pass


def get_watson_display_voice(voice: dict):
    person = (
            voice.get('Name')
            .replace(voice.get('Language') + '_', '')
            .replace('V3Voice', ' ')
            .replace('V2Voice', ' ')
            .replace('Voice', ' ')
    )
    data = person.split(' ')
    name = data[0]
    return name


class TtsProxy(object):
    def __init__(self):
        self.will_read= None
        self.using_the_voice_of= 'en-US_AllisonV3Voice'

    def update_reading(self, text):
        self.will_read = text

    def update_speaking_voice(self, to_voice):
        self.using_the_voice_of = to_voice

    def get_text_to_read(self) -> str:
        return self.will_read

    def get_voice_that_will_read(self):
        return self.using_the_voice_of

    pass


proxy = TtsProxy()


@eel.expose
def on_read(text=None):
    eel.reading()
    eel.sleep(4)


    # region guard condition for text
    if text is None or text == '' or text == ' ' * len(text):
        message = "You've, provided an invalid text!"
        eel.display_error(message)
        raise EmptyTextError(text, message)
    # endregion guard condition for text

    # region  process text

    # check difference between text on param and proxy: if hs not changed
    if proxy.get_text_to_read() != text:
        proxy.update_reading(text)
        say(phrase=proxy.get_text_to_read(), voice=proxy.get_voice_that_will_read())
    else:
        audio_segment = audio_player.get_audio_segment(os.path.join(temp_audio_folder, "sample_phrase.mp3"))
        audio_player.play_audio_segment(audio_segment)
    # endregion

    eel.sleep(4)
    eel.done_reading()
    pass


@eel.expose
def on_voice_changed(voice):
    proxy.update_speaking_voice(voice)
    pass


render()

eel.start('main.html', port=1989, size=(500, 600))
