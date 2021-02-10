
function show_or_hide_tts_control_area(){
    if( get_main_text_area().value.length > 0)
        get_tts_control_area().style = 'display: block; animation: fade-in 3s ease-in-out forwards;';
    else
        get_tts_control_area().style = 'animation: fade-out 2s ease-in-out; display: none;';
}

// region elements
function get_tts_audio_area(){
    return document.getElementById("tts_audio_area");
}


function get_main_text_area(){
    return document.getElementById("main_text_area");
}

function get_tts_control_area(){
    return document.getElementById("tts_control_area");
}

function get_read_button(){
    return document.getElementById("read_button");
}

function get_voices(){
    return document.getElementById("voices");
}

function get_display_voice(voice){
    return eel.get_watson_display_voice(voice);
}
// endregion

function sleep(s) {
  return new Promise(resolve => setTimeout(resolve, s * 1000));
}

// region interfaces
function on_read(){
    eel.on_read(get_main_text_area().value);
}

function on_voice_selected(){
    var voice = document.querySelector('#voices option:checked');
    eel.on_voice_changed(voice.getAttribute('value'));
}

function render_male_voices(){
    return eel.render_male_voices()
}
// endregion


// region callbacks
eel.expose(display_error);
function display_error(message){
    alert(message);
    ready_to_read();
    show_or_hide_tts_control_area();
}

eel.expose(reading);
function reading(){
    read_button = get_read_button();
    read_button.textContent = "Reading...";
    read_button.style = "animation: change_to_reading_state 4s ease-in;";
    read_button.style = "background-color: orange;";
}


eel.expose(done_reading);
function done_reading(){
    read_button = get_read_button();
    read_button.textContent = "Done reading!";
    read_button.style = "animation: change_to_done_state 4s ease-in-out;";
    read_button.style = "background-color: red;";
    sleep(2).then(() => {
        // Do something after the sleep!
        ready_to_read();
    });
}


function ready_to_read(){
    read_button = get_read_button();
    read_button.textContent = "Read";
    read_button.style = "animation-name: change_to_ready_state; animation-duration: 5s;";
    sleep(2).then(() => {
        // Do something after the sleep!
        read_button.style = "background-color: green;";
    });
}
// endregion

