class Websockets_title {
    static generate_session_id() {
        const timestamp = new Date().getTime();
        const randomNumber = Math.floor(Math.random() * 1000000);
        const sessionID = `${user_id}-${title_id}-${timestamp}-${randomNumber}`;

        return sessionID;
    }

    handler_websocket_response() {    
        ws.onmessage = function(event) {
            const response = JSON.parse(event.data);
            const is_onopen = response.websockets_csrf_token != null; 
            const websocket_type = response.type;

            if (is_onopen) {
                for (let websocket_type in websockets_types)
                    websockets_types[websocket_type].create_websoket_data(response, websocket_type);
            }
            else 
                websockets_types[websocket_type].update_elements(response);
        };
    }

    create_websoket_data(response, websocket_type) {
        this.websoket_data = JSON.stringify({
            type: websocket_type,
            user_id: user_id,
            title_id: title_id,
            websockets_csrf_token: response.websockets_csrf_token
        });            
    }

    send_websocket(websoket_data) {
        if (!user_id) return window.location.href = "/signin";

        ws.send(websoket_data)
    }

    listen_websocket_close() {
        ws.onclose = () => location.reload();
    }
}