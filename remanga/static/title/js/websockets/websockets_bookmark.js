class Websockets_bookmark extends Websockets_title {
    constructor() {
        super();

        this.bookmark_button = document.querySelector(".Button_bookmark");
        this.title_count_bookmarks = document.querySelector(".title_count_bookmarks");

        this.bookmark_button.addEventListener("click", () => super.send_websocket(this.websoket_data))
    }

    update_elements(response) {
        if (response.title_dir_name != title_dir_name) return;

        const title_count_bookmarks_int = Number(this.title_count_bookmarks.innerHTML);
        const is_bookmark_added = this.bookmark_button.innerText == "ДОБАВИТЬ В СПИСОК";

        this.bookmark_button.innerHTML = is_bookmark_added ? 
            "УБРАТЬ ИЗ СПИСКА" : "ДОБАВИТЬ В СПИСОК";

        this.title_count_bookmarks.innerHTML = is_bookmark_added ? 
            title_count_bookmarks_int + 1 : title_count_bookmarks_int - 1;
    }
}