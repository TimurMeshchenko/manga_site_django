class Chapters_filters {
  constructor() {
    this.url_params = ["count_chapters_gte", "count_chapters_lte"];
    this.param_gte = "count_chapters_gte";
    this.param_lte = "count_chapters_lte";

    const chapters_spans = [...document.querySelectorAll(".Chip_chip__cpsxK")];
    
    this.listen_chapters(chapters_spans)
    this.init_url_chapters_map();

    this.is_not_chapters_selected =
      !this.url_chapters_map[this.param_gte] &&
      !this.url_chapters_map[this.param_lte];

    this.color_chapters(chapters_spans);
  }

  listen_chapters(chapters_spans) {
    this.first_index_chapters_spans = 0;
    this.last_index_chapters_spans = chapters_spans.length - 1;

    for (const chapter_span of chapters_spans) {
      chapter_span.addEventListener("click", (event) => {
        const chapters_range = event.target.innerText.split("-");
        chapters_range[0] = chapters_range[0].replace(/\D/g, "");
        this.index_clicked_chapter = chapters_spans.indexOf(event.target);
        
        this.fill_empty_range_value(chapters_range)
        this.get_url_data_and_change_url(chapters_range)
      });
    }
  }

  fill_empty_range_value(chapters_range) {
    if (this.index_clicked_chapter == this.first_index_chapters_spans) {
      chapters_range.unshift(String());
    } else {
      chapters_range.push(String());
    }
  }

  get_url_data_and_change_url(chapters_range) {
    const have_drop_menu = false;
    const url_data = new Drop_menu_url_requests().get_url_data(
      this.url_params,
      chapters_range,
      have_drop_menu
    );

    this.change_url(url_data);
  }

  init_url_chapters_map() {
    this.url_chapters_map = new Object();
    for (let search_part of window.location.search.split("&")) {
      for (let url_param of this.url_params) {
        if (search_part.includes(url_param)) {
          this.url_chapters_map[url_param] = search_part.replace(/\D/g, "");
        }
      }
    }
  }

  color_chapters(chapters_spans) {
    const storage_indices_clicked_chapters = JSON.parse(
      localStorage.getItem("indices_clicked_chapters")
    );
    const chapter_class_gray = "Chip_gray__uE26d";
    const chapter_class_blue = "Chip_primary__AHVQ0";

    if (this.remove_empty_storage_clicked_chapters(storage_indices_clicked_chapters))
      return

    for (let index_clicked_chapter of storage_indices_clicked_chapters) {
      chapters_spans[index_clicked_chapter].className = chapters_spans[
        index_clicked_chapter
      ].className.replace(chapter_class_gray, chapter_class_blue);
    }
  }

  remove_empty_storage_clicked_chapters(storage_indices_clicked_chapters) {
    if (
      storage_indices_clicked_chapters == null ||
      !window.location.search.includes(this.param_gte) ||
      storage_indices_clicked_chapters.length == 0
    ) {
      localStorage.removeItem("indices_clicked_chapters");
      return true;
    }

    return false;
  }

  change_url(url_data) {
    let new_url_requests_array = url_data[0];
    this.url_repeats_map = url_data[1];

    this.url_change_value(new_url_requests_array);

    let url_replaced = new_url_requests_array.join("");
    if (!url_replaced.includes("?")) {
      url_replaced = url_replaced.replace("&", "?");
    }

    this.save_index_clicked_chapter();

    window.location.search = url_replaced;
  }

  url_change_value(new_url_requests_array) {
    const is_not_url_chapters_selected = !window.location.search.includes(this.param_gte) ||
    this.replace_empty_url_chapters_values(new_url_requests_array);

    if (is_not_url_chapters_selected) return;
  
    this.all_chapter_values = [
      Object.values(this.url_chapters_map),
      Object.values(this.url_repeats_map),
    ]
      .flatMap((subArr) => subArr)
      .map(Number);

    this.remove_chapters_filters();
    this.replace_zero_to_empty_and_update_new_url(new_url_requests_array);
  }

  replace_empty_url_chapters_values(new_url_requests_array) {
    const count_chapters_divs = 4;
    const storage_indices_clicked_chapters = JSON.parse(
      localStorage.getItem("indices_clicked_chapters")
    );

    const is_all_chapters_selected = storage_indices_clicked_chapters != null &&
    storage_indices_clicked_chapters.length === count_chapters_divs;

    const is_chapters_selected = !this.is_not_chapters_selected || is_all_chapters_selected;

    if (is_chapters_selected) return false;

    for (let url_param of this.url_params) {
      this.replace_old_url_chapter_request(
        new_url_requests_array,
        url_param
      );
    }

    return true;
  }

  replace_old_url_chapter_request(new_url_requests_array, url_param) {
    for (let i = 0; i < new_url_requests_array.length; i++) {
      if (new_url_requests_array[i].includes(url_param)) {
        let url_request_name = new_url_requests_array[i].split("=")[0];
        new_url_requests_array[
          i
        ] = `${url_request_name}=${this.url_repeats_map[url_param]}`;
      }
    }
  }

  remove_chapters_filters() {
    this.filtered_all_chapter_values = this.all_chapter_values;
    let set_all_chapter_values = [...new Set(this.all_chapter_values)];
    const is_clicked_to_same_chapters = this.filtered_all_chapter_values.length !== set_all_chapter_values.length;

    if (is_clicked_to_same_chapters) {
      this.remove_dublicates_chapter_values();
      this.clear_all_chapter_values_gte_empty();
    } else {
      this.clicked_second_or_last_chapter_span()
    }

    this.add_gte_or_lte_for_empty_url_chapters()

    this.url_repeats_map[this.param_gte] = Math.min(
      ...this.filtered_all_chapter_values
    );
    this.url_repeats_map[this.param_lte] = Math.max(
      ...this.filtered_all_chapter_values
    );

    this.reverse_url_repeats_values();
  }

  remove_dublicates_chapter_values() {
    for (let chapter_value of this.filtered_all_chapter_values) {
      if (
        this.filtered_all_chapter_values.indexOf(chapter_value) !==
        this.filtered_all_chapter_values.lastIndexOf(chapter_value)
      ) {
        this.filtered_all_chapter_values =
          this.filtered_all_chapter_values.filter(
            (item) => item !== chapter_value
          );
      }
    }
  }

  clear_all_chapter_values_gte_empty() {
    const index_gte_value = 0;
    const is_clicked_last_chapter = this.index_clicked_chapter == this.last_index_chapters_spans;
    const only_chapters_lte_exist = Object.values(this.url_chapters_map).lastIndexOf("") == index_gte_value;

    if (
      this.filtered_all_chapter_values == false || is_clicked_last_chapter && only_chapters_lte_exist
    ) {
      this.clear_all_chapter_values()
    }
  }

  clear_all_chapter_values() {
    this.filtered_all_chapter_values = [0, 0];
  }

  clicked_second_or_last_chapter_span() {
    const second_index_chapters_spans = 1;

    if (
      this.index_clicked_chapter == second_index_chapters_spans ||
      this.index_clicked_chapter == this.last_index_chapters_spans
    ) {
      this.replace_chapters_values_to_min_gte_and_lte()
    }
  }

  replace_chapters_values_to_min_gte_and_lte() {
    const sorted_chapter_values = this.filtered_all_chapter_values.sort(
      (a, b) => a - b
    );
    
    this.filtered_all_chapter_values = [sorted_chapter_values[0], sorted_chapter_values[1]]
  }

  add_gte_or_lte_for_empty_url_chapters() {
    if (this.is_not_chapters_selected) {
      this.filtered_all_chapter_values.unshift(0);

      if (
        this.index_clicked_chapter !== this.first_index_chapters_spans &&
        this.index_clicked_chapter !== this.last_index_chapters_spans
      ) {
        this.filtered_all_chapter_values.pop();
      }
    }
  }

  reverse_url_repeats_values() {
    const index_lte_value = 1;
    const first_empty_chapters_index = Object.values(this.url_chapters_map).indexOf("");
    
    const is_only_gte_exist = first_empty_chapters_index == index_lte_value;
    const is_first_chapter_clicked = this.index_clicked_chapter == this.first_index_chapters_spans;

    if (this.is_need_to_clean_lte()) {
      const all_chapters_selected = is_only_gte_exist && is_first_chapter_clicked;
     
      if (all_chapters_selected) {
        this.clear_all_chapter_values()
      }

      this.url_repeats_map[this.param_lte] = Math.min(
        ...this.filtered_all_chapter_values
      );
      this.url_repeats_map[this.param_gte] = Math.max(
        ...this.filtered_all_chapter_values
      );
    }
  }

  is_need_to_clean_lte() {
    const index_lte_value = 1;
    const first_empty_chapters_index = Object.values(this.url_chapters_map).indexOf("");
    const is_only_gte_exist = first_empty_chapters_index == index_lte_value;
   
    const is_first_chapter_clicked = this.index_clicked_chapter == this.first_index_chapters_spans;
    const is_both_chapters_values_exist = first_empty_chapters_index == -1;
    const is_last_chapter_clicked = this.index_clicked_chapter == this.last_index_chapters_spans;

    const is_need_to_clean_lte = (is_only_gte_exist && !is_last_chapter_clicked) ||
      (is_both_chapters_values_exist && is_last_chapter_clicked) ||
      (this.is_not_chapters_selected && is_first_chapter_clicked)
    
    return is_need_to_clean_lte;
  }

  replace_zero_to_empty_and_update_new_url(new_url_requests_array) {
    for (let url_param of this.url_params) {
      if (this.url_repeats_map[url_param] == 0)
        this.url_repeats_map[url_param] = "";

      this.replace_old_url_chapter_request(new_url_requests_array, url_param);
    }
  }

  save_index_clicked_chapter() {
    let storage_indices_clicked_chapters = JSON.parse(
      localStorage.getItem("indices_clicked_chapters")
    );

    this.indices_clicked_chapters = [this.index_clicked_chapter];

    if (storage_indices_clicked_chapters !== null) {
      storage_indices_clicked_chapters = 
        this.add_previous_indices_clicked_chapters(storage_indices_clicked_chapters);
      
      this.set_colors(
        storage_indices_clicked_chapters
      );
    }

    localStorage.setItem(
      "indices_clicked_chapters",
      JSON.stringify(this.indices_clicked_chapters)
    );
  }

  add_previous_indices_clicked_chapters(storage_indices_clicked_chapters) {
    storage_indices_clicked_chapters =
      storage_indices_clicked_chapters.flatMap((subArr) => subArr);

    this.indices_clicked_chapters.push(storage_indices_clicked_chapters);
    this.indices_clicked_chapters = this.indices_clicked_chapters.flatMap(
      (subArr) => subArr
    );

    return storage_indices_clicked_chapters;
  }

  set_colors(storage_indices_clicked_chapters) {
    const is_clicked_new_chapters = storage_indices_clicked_chapters.indexOf(this.index_clicked_chapter) == -1;
    
    if (is_clicked_new_chapters)
      this.add_colors();
    else 
      this.remove_colors();
  }

  add_colors() {
    const all_chapters_indexes = [0, 1, 2, 3];

    this.indices_clicked_chapters = all_chapters_indexes.slice(
      Math.min(...this.indices_clicked_chapters),
      Math.max(...this.indices_clicked_chapters) + 1
    );
  }

  remove_colors() {
    const indices_clicked_chapters_without_duplicate = this.indices_clicked_chapters.shift();
    const is_clicked_first_or_last_chapters = this.index_clicked_chapter == this.first_index_chapters_spans ||
      this.index_clicked_chapter == this.last_index_chapters_spans;

    const is_activated_second_and_third_chapters = (!this.indices_clicked_chapters.includes(this.first_index_chapters_spans) &&
      !this.indices_clicked_chapters.includes(this.last_index_chapters_spans));

    if (is_clicked_first_or_last_chapters || is_activated_second_and_third_chapters)
      this.remove_one_color();
    else 
      this.remove_multiple_colors();
  }

  remove_one_color() {
    this.indices_clicked_chapters = this.indices_clicked_chapters.filter(
      (item) => item !== this.index_clicked_chapter
    );
  }

  remove_multiple_colors() {
    const is_not_activated_first_chapter = this.indices_clicked_chapters.indexOf(this.first_index_chapters_spans) == -1;

    if (is_not_activated_first_chapter)
      this.remove_colors_from_left_to_right()
    else
      this.remove_colors_from_right_to_left()
  }

  remove_colors_from_left_to_right() {
    this.indices_clicked_chapters = this.indices_clicked_chapters.slice(
      this.indices_clicked_chapters.indexOf(this.index_clicked_chapter) + 1,
      Math.max(...this.indices_clicked_chapters)
    );
  }

  remove_colors_from_right_to_left() {
    this.indices_clicked_chapters = this.indices_clicked_chapters.slice(
      Math.min(...this.indices_clicked_chapters),
      this.index_clicked_chapter
    );
  }
}