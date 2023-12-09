class Drop_menu_url_requests {
  constructor() {}

  get_url_data(names, values, have_drop_menu = true) {
    this.url_repeats_array = Array();
    this.new_url_requests_array = [window.location.search.split("&")[0]];

    for (let i = 1; i < window.location.search.split("&").length; i++) {
      this.new_url_requests_array.push(
        `&${window.location.search.split("&")[i]}`
      );
    }

    for (let i = 0; i < names.length; i++) {
      let separator =
        this.new_url_requests_array[0] == `?${names[i]}=${values[i]}`
          ? "?"
          : "&";

      if (have_drop_menu) {
        this.init_arrays_drop_menu(separator, names[i], values[i]);
      } else {
        this.init_arrays_not_drop_menu(separator, names[i], values[i]);
      }
    }

    return [this.new_url_requests_array, this.url_repeats_array];
  }

  init_arrays_drop_menu(separator, name, value) {
    if (
      this.new_url_requests_array.indexOf(`${separator}${name}=${value}`) == -1
    ) {
      this.new_url_requests_array.push(`${separator}${name}=${value}`);
    } else {
      this.get_url_repeats_array(separator, name, value);
    }
  }

  init_arrays_not_drop_menu(separator, name, value) {
    if (!this.new_url_requests_array.join("").includes(name)) {
      this.new_url_requests_array.push(`${separator}${name}=${value}`);
    } else {
      this.url_repeats_array[name] = value;
    }
  }

  get_url_repeats_array(separator, name, value) {
    if (this.url_repeats_array.indexOf(`${separator}${name}=${value}`) == -1) {
      this.url_repeats_array.push(`${separator}${name}=${value}`);
    } else {
      this.url_repeats_array = this.url_repeats_array.filter(
        (item) => item !== `${separator}${name}=${value}`
      );
    }
  }

  delete_label(event, current_index_clicked_element, data_array, url_params) {
    const label_class = ".jsx-9f9056eddaf3b30b";
    const label_text =
      event.target.parentNode.querySelector(label_class).innerText;

    const divs_inputs = document.querySelectorAll(".jsx-d338f3d1a4c6e9b5");
    const count_exclude_filters = 3;
    const exclude_data_index = divs_inputs.length - count_exclude_filters;
    let _current_index_clicked_element = current_index_clicked_element;

    if (current_index_clicked_element >= exclude_data_index) {
      _current_index_clicked_element -= exclude_data_index;
    }

    const data = data_array[_current_index_clicked_element];
    let value_key = Object.keys(data[0]);
    value_key = value_key[value_key.length - 1];

    for (let index_text = 0; index_text < data.length; index_text++) {
      if (data[index_text][value_key] == label_text) {
        return this.get_url_data(
          [url_params[current_index_clicked_element]],
          [index_text]
        );
      }
    }
  }
}
