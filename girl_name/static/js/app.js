function change_choice(my_url, status_choice) {
    let token = document.querySelector('#p-token');
    fetch(
        my_url,
        {
            method: 'PATCH', headers: {"X-CSRFToken": token.innerText,'Content-type': 'application/json'},
            body: JSON.stringify({choice: status_choice})
        }
    )
        .then(
            function (resp) {
                if (!resp.ok) {
                    alert('Wystąpił błąd! Otwórz devtools i zakładkę Sieć/Network, i poszukaj przyczyny');
                }
                return resp.json()
            })
}

function switch_choices(switch_buttons, yes, no, maybe) {

    function change_border() {
        for (let button of switch_buttons) {
            button.classList.remove('border-active');
        }
        this.classList.add('border-active');
    }

    function switch_names() {
        yes.classList.add('d-none');
        no.classList.add('d-none');
        maybe.classList.add('d-none');

        if (this.innerText === 'Tak') {
            yes.classList.remove('d-none');
        } else if (this.innerText === 'Nie') {
            no.classList.remove('d-none');
        } else {
            maybe.classList.remove('d-none');
        }
    }

    Array.from(switch_buttons).forEach(element => {
        element.addEventListener('click', function (event) {
            event.preventDefault();
            change_border.call(this);
            switch_names.call(this);

        })
    })
}

function patch_choice(names, switch_buttons, yes, no, maybe) {
    function drop_to_db(my_url) {
        if (this.innerText === 'Tak') {
            let li = document.createElement('li');
            li.appendChild(selected_name);
            yes.prepend(li);
            change_choice(my_url, 0);

        } else if (this.innerText === 'Nie') {
            let li = document.createElement('li');
            li.appendChild(selected_name);
            no.prepend(li);
            change_choice(my_url, 1);

        } else {
            let li = document.createElement('li');
            li.appendChild(selected_name);
            maybe.prepend(li);
            change_choice(my_url, 2);

        }
    }

    names.forEach(name => {
        name.addEventListener('dragstart', function (event) {
            selected_name = event.target;
        })

        Array.from(switch_buttons).forEach(button => {
            button.addEventListener('dragover', function (event) {
                event.preventDefault();
            })
            button.addEventListener('drop', function (event) {
                event.preventDefault();
                event.stopImmediatePropagation();
                let my_url = '/girl-name/serializer/' + selected_name.dataset.id
                drop_to_db.call(this, my_url);
            })
        })

    })
}

document.addEventListener('DOMContentLoaded', function () {
    const switch_buttons = document.querySelector('#over_buttons').children;
    const yes = document.querySelector('#ul-yes');
    const no = document.querySelector('#ul-no');
    const maybe = document.querySelector('#ul-maybe');
    const names = document.querySelectorAll('.wide-div a');

    switch_choices(switch_buttons, yes, no, maybe);
    patch_choice(names, switch_buttons, yes, no, maybe);
})