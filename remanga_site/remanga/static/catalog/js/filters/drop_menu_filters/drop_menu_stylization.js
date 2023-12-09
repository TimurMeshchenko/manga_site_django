class Drop_menu_stylization {
  constructor() {
    this.url_search = window.location.search.replace("?", "");
    this.divs_label = document.querySelectorAll(".jsx-df39090361a5f2e4");
    this.label_class = "select-option";
    this.drop_menu_element = document.querySelector(".jsx-f6904a6ed8e0085");
  }

  color_clicked_span(url_param, url_search = this.url_search) {
    const all_drop_menu_spans = [
      ...document.querySelectorAll(".jsx-1b57bf17c694e838"),
    ];
    const selected_elements = document.querySelectorAll(".item-selected");

    for (let selected_element of selected_elements) {
      selected_element.classList.remove("item-selected");
    }

    if (!url_search || this.drop_menu_element == null) {
      return;
    }

    for (let url_part of url_search.split("&")) {
      const url_part_key = url_part.split("=")[0]; 
      const url_part_value = url_part.split("=")[1]; 

      if (url_part_key == url_param) {
        let drop_menu_span = all_drop_menu_spans[url_part_value] 
        
        if (drop_menu_span !== undefined) {
          drop_menu_span.classList.add("item-selected");
        }
      }
    }
  }

  add_label_input(url_params, data_array, url_search = this.url_search) {
    const label_elements = document.querySelectorAll(".jsx-9f9056eddaf3b30b");

    for (let label_element of label_elements) {
      label_element.remove();
    }

    for (let url_part of url_search.split("&")) {
      let have_drop_menu = url_params.some((substring) =>
        url_part.includes(substring)
      );
      if (!have_drop_menu) {
        continue;
      }

      this.init_label_input(url_part, url_params, data_array);

      if (this.drop_menu_element) {
        this.change_drop_menu_height(this.index_url_part_name);
      }
    }
    this.remove_placeholder();
  }

  init_label_input(url_part, url_params, data_array) {
    const url_part_value = url_part.replace(/\D/g, "");
    const url_part_name = url_part.replace(`=${url_part_value}`, String());
    this.index_url_part_name = url_params.indexOf(url_part_name);

    if (!url_part_name || this.index_url_part_name == -1) {
      return;
    };

    const div_label = this.divs_label[this.index_url_part_name];
    const max_count_labels = 6;
    const all_existing_labels = div_label.querySelectorAll(
      `.${this.label_class}`
    );
      
    if (all_existing_labels.length < max_count_labels) {
      const label_name = this.get_label_name(data_array, url_part_value);
      this.insert_label_html(div_label, label_name)
    }
  }

  get_label_name(data_array, url_part_value) {
    const count_exclude_filters = 3;
    const exclude_data_index = this.divs_label.length - count_exclude_filters;
    let total_index_url_part_name = this.index_url_part_name;

    if (this.index_url_part_name >= exclude_data_index) {
      total_index_url_part_name -= exclude_data_index;
    }

    const data = data_array[total_index_url_part_name];
    let value_key = Object.keys(data[0]);
    value_key = value_key[value_key.length - 1];
    const label_name = data[url_part_value][value_key];

    return label_name
  }

  insert_label_html(div_label, label_name) {
    div_label.insertAdjacentHTML(
      "afterbegin",
      `
          <span role="listitem" class="jsx-9f9056eddaf3b30b select-option">
            <span class="jsx-9f9056eddaf3b30b">${label_name}</span>
            <span class="jsx-9f9056eddaf3b30b select-option-remove">×</span>
          </span>
        `
    );
  }

  remove_placeholder() {
    for (const div_label of this.divs_label)
      if (div_label.innerHTML.includes(this.label_class)) {
        div_label.querySelector("input").placeholder = String();
      }
  }

  change_drop_menu_height(index_clicked_element) {
    if (index_clicked_element == -1) {
      return;
    }

    const div_label_parent = this.divs_label[index_clicked_element].parentNode;
    const drop_menu_class = `.${this.drop_menu_element.classList[0]}`;

    if (div_label_parent.querySelector(drop_menu_class) !== null) {
      this.drop_menu_element.style["top"] = `${
        this.divs_label[index_clicked_element].offsetHeight + 2
      }px`;
    }
  }

  search_color_span(item_selected) {
    const all_drop_menu_spans = [
      ...document.querySelectorAll(".jsx-1b57bf17c694e838"),
    ];

    all_drop_menu_spans.forEach((span) => {
      item_selected.forEach((selected) => {
        if (span.ariaLabel === selected.ariaLabel) {
          span.classList.add("item-selected");
        }
      });
    });
  }
}
