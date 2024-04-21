const grid = document.querySelector(".grid");
const input = document.querySelector(".Input_input__F9Zao");
const titles = JSON.parse(titles_json);
const empty_grid_html = grid.innerHTML;

const page_size = 30;
const search_endless_scroll = new Search_endless_scroll();
let pages_count = Math.floor(titles.length / page_size);
let filtered_titles = titles;

search_endless_scroll.add_titles_page(filtered_titles)
input.addEventListener("keyup", update_filtered_titles); 

function update_filtered_titles(event) {
    grid.innerHTML = empty_grid_html;

    filtered_titles = titles.filter((title) =>
      title["rus_name"].toLowerCase().includes(event.target.value.toLowerCase())
    );

    search_endless_scroll.page = 0;
    pages_count = Math.floor(filtered_titles.length / page_size);
    
    if (filtered_titles.length > 0) {
      update_endless_scroll_gridPlaceholder();
      search_endless_scroll.add_titles_page(filtered_titles)
    }
    else {
      grid.innerHTML = `<b>No results found...</b>`
      update_endless_scroll_gridPlaceholder();
    }    
}

function update_endless_scroll_gridPlaceholder() {
    search_endless_scroll.gridPlaceholder = search_endless_scroll.grid.querySelector(".gridPlaceholder");
}

function add_title(title) {
    search_endless_scroll.gridPlaceholder.insertAdjacentHTML(
      "beforebegin",
      `              
      <div class="gridItem">
        <a
          title="${title["rus_name"]}"
          class="Vertical_card__Sxft_"
          href="/manga/${title["dir_name"]}">
          <div class="Vertical_wrapper__eThs_">
            <div
              class="Image_container__NpLCh Image_hover__XbAZP rounded-md Vertical_img__vaURH Image_imagePlaceholder__oa9r1">
              <div
                class="Image_imgStatic__14_gQ Image_image__HOj0m Image_imgFluid__Men3E Image_lazyLoaded__VDjoe"
                style="background-image: url('/manga/media/titles/${
                  title["img_url"]
                }');">
              </div>
            </div>
            <div class="Vertical_rating__nY5Rc">${title["avg_rating"].toFixed(
              1
            )}</div>
            <div class="Horizontal_title_info">
              <p class="Typography_caption__yY5RL">
                ${title["manga_type"]}
              </p>
              <h4 class="Typography_h6__crs2H Typography_lineClamp-2__4Ampt Typography_lineClamp__92oq_">
                ${title["rus_name"]}
              </h4>
            </div>
          </div>
        </a>
      </div>
    `
    );
}