const chatInput = $("#chat-input")[0];
const utf8Decoder = new TextDecoder('UTF-8');
const conversationPanel = $(".conversation-panel")[0];
let is_reading_from_stream = false;
let conversation = [];
let temporary_string = "";

$(() => {
    fetch("/history").then(
        (response) => response.json().then((value) => renderHistory(value))
    )
});

chatInput.addEventListener("keyup", ({ key, shiftKey }) => {
    if (key === "Enter" && !shiftKey && !is_reading_from_stream) {
        if (!handleCommand(chatInput.value)) {
            addUserDialogue(chatInput.value);

            scrollConversationPanel();
            chat(chatInput.value);
        }

        chatInput.value = "";
    }
});

function preprocessContent(content) {
    content = content.replaceAll("\n", "<br>");
    content = content.replaceAll(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    content = content.replaceAll(/\*(.+?)\*/g, "<i>$1</i>");
    content = content.replaceAll(/`(.+?)`/g, "<samp>$1</samp>");
    content = content.replaceAll(/###(.+?)<br>/g, "<h3>$1</h3>");
    content = content.replaceAll(/##(.+?)<br>/g, "<h2>$1</h2>");
    content = content.replaceAll(/#(.+?)<br>/g, "<h1>$1</h1>");
    return content;
}

function createDialog({ role, content }) {
    let div = document.createElement('div');
    div.className = "dialogue-box " + (role == 'user' ? "query" : "answer");

    let p = document.createElement('p');
    p.className = "dialogue";
    p.innerHTML = preprocessContent(content);
    div.appendChild(p);

    return div;
}

function renderHistory(history) {
    history.forEach(el => {
        conversationPanel.appendChild(createDialog(el));
    });
}

function pumpReader(reader, chunk_callback, done_callback, state) {
    if (state.done) {
        done_callback();
        return;
    }

    chunk_callback(state.value);

    reader.read().then((state) => pumpReader(reader, chunk_callback, done_callback, state));
}

function readReader(reader, chunk_callback, done_callback) {
    reader.read().then((state) => pumpReader(reader, chunk_callback, done_callback, state));
}

function chat(text) {
    addToConversation('user', text);

    fetch("/chat", {
        method: "POST", headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({ 'messages': conversation })
    }).then(
        (value) => {
            let assistantDialogue = createDialog({ role: "assistant", content: "" });
            conversationPanel.appendChild(assistantDialogue);
            let textNode = assistantDialogue.childNodes[0];

            is_reading_from_stream = true;
            temporary_string = "";

            let reader = value.body.getReader();

            readReader(reader, (value) => {
                const new_chunk = utf8Decoder.decode(value);

                temporary_string += new_chunk;
                textNode.innerHTML = preprocessContent(textNode.innerHTML + new_chunk);

                scrollConversationPanel();
            }, () => { is_reading_from_stream = false; addToConversation('assistant', temporary_string) });
        })
}

function reset() {
    fetch("/history", { method: "DELETE" });
}

function addUserDialogue(text) {
    conversationPanel.appendChild(createDialog({ 'role': 'user', 'content': text }));
}

function handleCommand(text) {
    if (text[0] == "/") {
        text = text.substr(1);

        if (text == "reset") {
            reset();
            $(".conversation-panel")[0].innerHTML = "";
        }

        return true;
    }

    return false;
}

function scrollConversationPanel() {
    conversationPanel.scrollTop = conversationPanel.scrollHeight;
}

function addToConversation(role, content) {
    conversation.push({ 'role': role, 'content': content });
    console.log(conversation);
}