function load_urls() {
    toggle_loader(true);
    axios.get('/load_urls/').then((response) => {
        let urls = response.data;
        fill_table(urls['urls']);
        toggle_loader(false);
    })
}

function check_status() {
    toggle_loader(true);
    axios.get('/check_status/').then((response) => {
        load_urls();
    })
}

function change_check_status(e) {
    let button_caption = e.textContent;
    let status;
    if (button_caption === 'true') {
        button_caption = 'false';
        status = false;
    } else {
        button_caption = 'true';
        status = true;
    }
    e.textContent = button_caption;
    console.log(e.textContent);
    axios.post('/change_status/', {
        id: e.dataset['id'],
        check_status: status
    }).then((response) => {
        load_urls();
    })
}

function fill_table(url_list) {
    let tbody = document.getElementById('table_body');
    tbody.innerHTML = "";
    for (let i = 0; i < url_list.length; i++) {
        let row = JSON.parse(url_list[i]);
        let tr = document.createElement('tr');
        let td_id = document.createElement('td');
        let td_url = document.createElement('td');
        let td_check_status = document.createElement('td');
        let td_status_code = document.createElement('td');
        td_id.innerHTML = row.id;
        td_url.innerHTML = row.url;
        td_check_status.innerHTML = 
            `<button class="button 
                            is-secondary is-outlined" 
                    id="check_status" 
                    onclick="change_check_status(this)"
                    data-id="${row.id}"
            >${row.check_status}</button>`;
        td_status_code.innerHTML = row.status_code;
        td_status_code.classList.add("tag");
        td_status_code.classList.add("is-medium");
        td_status_code.classList.add("is-light");
        if (row.status_code == null || row.status_code == "") {
            td_status_code.classList.add("is-light");
            td_status_code.innerHTML = "-";
        } else if (row.status_code !== 200) {
            td_status_code.classList.add("is-danger");
        } else {
            td_status_code.classList.add("is-success");
        }
        tr.appendChild(td_id);
        tr.appendChild(td_url);
        tr.appendChild(td_check_status);
        tr.appendChild(td_status_code);
        tbody.appendChild(tr);
    }
}

function toggle_loader(val) {
    check_status_btn = document.getElementById('check_status');
    if (val === true) {
        if (check_status_btn.classList.contains('is-loading') === false) {
            check_status_btn.classList.add('is-loading');
        }
    } else {
        check_status_btn.classList.remove('is-loading');
    }
}

window.addEventListener("DOMContentLoaded", function () {
    load_urls();
}, false);