from natural_tts import get_language_attribute, get_voice_instance


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


if __name__ == '__main__':

    lang: dict = get_language_attribute()
    male_voices = get_gender_voices(get_voice_instance().get_all_male_voices_sorted())
    female_voices = get_gender_voices(get_voice_instance().get_all_female_voices_sorted())


    for lx, abbreviation in enumerate(lang.get('language_abbreviations')):
        print('\t', lang.get('languages')[lx])
        voices = male_voices.get(abbreviation)
        for vx, voice in enumerate(voices):
            previous_voice = voices[vx - 1] if vx > 0 else None
            shown_type = voice.get('Type')
            if previous_voice is None or (previous_voice.get('Type') != shown_type):
                print('\t\t', shown_type)

            print('\t\t\t', voice.get('Name'))
