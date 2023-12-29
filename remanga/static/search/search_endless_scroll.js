class Search_endless_scroll extends Endless_scroll {
    constructor() {
        super()
        this.page = 0
    }

    add_titles_page() {
        const start = this.page * page_size;
        const end = start + page_size;
        
        for (let i = start; i < end; i++) {
            if (i < filtered_titles.length)
                add_title(filtered_titles[i]);
        }
    }
}