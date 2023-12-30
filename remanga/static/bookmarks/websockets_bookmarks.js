function listen_websocket_response() {
    ws.onmessage = function (event) {
        const response = JSON.parse(event.data);
        const is_onopen = response.websockets_csrf_token != null;

        if (is_onopen || response.type != "bookmark") return;

        if (response.is_bookmark_added)
            add_title(response)
        else
            remove_removed_bookmark_title(response)
    }; 
}

function add_title(response) {
    add_title_html(response)
    
    const updated_last_title_element = get_last_title_element();
    const last_title_element_a = updated_last_title_element.querySelector("a");

    last_title_element_a.href = last_title_element_a.href.slice(0, -2) + response.title_dir_name;
}

function get_last_title_element() {
    const all_titles = document.querySelectorAll(".Grid_gridItem__aPUx1");
    const last_title_element = all_titles[all_titles.length - 1];
    return last_title_element;
}

function add_title_html(response) {
    const invisible_title_place = document.querySelector(".Grid_gridPlaceholder__2iCsF");

    invisible_title_place.insertAdjacentHTML("beforebegin", `
    <div class="Grid_gridItem__aPUx1 p-1"><a title="${response.title_rus_name}" class="Library_card__87Skx"
        href="${url_title_empty}">
        <div class="Library_wrapper__MWbWz">
            <div
                class="Image_container__z9DC9 Image_hover__3aJFw rounded-sm Library_img__ASP_l Image_imagePlaceholder__7plww">
                <div class="Image_imgStatic__qYXY7 Image_image__85Rxf Image_imgFluid__7ygPD Image_lazyLoaded__LVajX"
                    alt="Обложка произведения ${response.title_rus_name}"
                    style="background-image: url('/media/titles/${response.title_img_url}');">
                </div>
            </div>
        </div>
        <div class="Library_cardTitle__AgujO Library_unreadFree__ZWBJg">
            <h4
                class="Typography_h6__VMBDX Typography_lineClamp-2__A03jO Typography_lineClamp__Pa1wi">
                ${response.title_rus_name}</h4>
        </div>
    </a>
    </div>
    `);
}

function remove_removed_bookmark_title(response) {
    const titles_a_elements = document.querySelectorAll(".Library_card__87Skx"); 
    
    for (const title_a_element of titles_a_elements) {
        if (title_a_element.title == response.title_rus_name)
            return title_a_element.parentElement.remove();
    }
}