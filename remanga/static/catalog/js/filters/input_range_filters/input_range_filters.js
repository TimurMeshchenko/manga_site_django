class Input_range_filters {
  constructor() {
    this.url_params = [
      "issue_year_gte",
      "issue_year_lte",
      "rating_gte",
      "rating_lte",
    ];
    this.timer;
    this.url_replaced = Array();
    this.names_clicked_inputs = Array();
    this.input_values = Array();

    this.listen_input_range();
  }

  listen_input_range() {
    const inputs = [...document.querySelectorAll(".Input_input__F9Zao")];
    for (let input of inputs) {
      input.addEventListener("keyup", (event) => {
        this.index_clicked_input = inputs.indexOf(event.target);
        this.names_clicked_inputs.push(
          this.url_params[this.index_clicked_input]
        );
        this.input_values.push(input.value);
        const url_data = new Drop_menu_url_requests().get_url_data(
          this.names_clicked_inputs,
          this.input_values,
          false
        );

        this.change_url(url_data);
      });
    }

    this.restore_input_range(inputs);
  }

  change_url(url_data) {
    let new_url_requests_array = url_data[0];
    let url_repeats_map = url_data[1];

    this.url_change_value(new_url_requests_array, url_repeats_map);
    this.url_replaced = new_url_requests_array.join("");

    if (!this.url_replaced.includes("?")) {
      this.url_replaced = this.url_replaced.replace("&", "?");
    }

    if (this.timer !== undefined) {
      clearTimeout(this.timer);
    }

    this.timer = setTimeout(() => {
      localStorage.setItem("index_clicked_input", this.index_clicked_input);

      window.location.search = this.url_replaced;
    }, 700);
  }

  url_change_value(new_url_requests_array, url_repeats_map) {
    for (let url_param of this.url_params) {
      if (url_repeats_map[url_param] == undefined) {
        continue;
      }

      for (let i = 0; i < new_url_requests_array.length; i++) {
        if (new_url_requests_array[i].includes(url_param)) {
          let url_request_name = new_url_requests_array[i].split("=")[0];
          new_url_requests_array[i] = `${url_request_name}=${url_repeats_map[url_param]}`;
        }
      }
    }
  }

  restore_input_range(inputs) {
    const saved_index_clicked_input = localStorage.getItem(
      "index_clicked_input"
    );

    if (saved_index_clicked_input !== null) {
      inputs[saved_index_clicked_input].focus();
      localStorage.removeItem("index_clicked_input");
    }

    for (let search_part of window.location.search
      .replace("?", "")
      .split("&")) {
      let is_input_range = this.url_params.some((substring) =>
        search_part.includes(substring)
      );
      if (!is_input_range) {
        continue;
      }

      let index_url_param = this.url_params.indexOf(search_part.split("=")[0]);
      inputs[index_url_param].value = search_part.split("=")[1];
    }
  }
}
